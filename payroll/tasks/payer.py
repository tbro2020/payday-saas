from concurrent.futures import ThreadPoolExecutor, as_completed
from employee import models as employee_model
from django.db.models import Sum, Q
from django.conf import settings
import os

from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from core.models import Notification
from payroll.models import *

from celery import Task
import pandas as pd

from dask.distributed import Client
from datetime import datetime
from payday.celery import app
import json

remove_leading_zero = lambda x: str(int(x)) if x and x.isdigit() else x

class Payer(Task):
    """
    Celery Task to handle payroll processing and payslip generation.
    """
    errors = []
    name = 'payer'
    ignore_result = True   
    string_fields = ['matricule', 'registration_number']

    def run(self, pk, *args, **kwargs):
        """
        Main entry point for the task. Processes the payroll.
        """
        DEBUG = settings.DEBUG
        self.now = datetime.now()
        self.today = self.now.today
        self.chunks_size = int(getattr(settings, 'PAYROLL_CHUNCKS_SIZE', 100))
        
        self.workers = os.cpu_count() * (1.0 if DEBUG else 1.5)
        self.payroll = get_object_or_404(Payroll, pk=pk)

        # Load additional items from Excel
        self.canvas = self.load_excel(self.payroll.canvas)
        self.additional_items = self.load_excel(self.payroll.additional_items)
        if not self.additional_items.empty:
            self.additional_items = self.re_base_additional_element_column(self.additional_items)
        
        self.legal_items = LegalItem.objects.all()
        self.items = Item.objects.exclude(Q(condition='0') | Q(condition__isnull=True)).order_by('code')

        # Build and apply employee filter
        self.employees = employee_model.Employee.objects.select_related().all()
        self.employees = self.employees.filter(**{
            k:v for k, v in {
                'grade__in': self.payroll.employee_grade.values_list('id', flat=True),
                'branch__in': self.payroll.employee_branch.values_list('id', flat=True),
                'status__in': self.payroll.employee_status.values_list('id', flat=True),
                'direction__in': self.payroll.employee_direction.values_list('id', flat=True)
            }.items() if v
        }).filter(**kwargs.get('employee', {})).order_by('-registration_number')

        # Set the maximum count of employees
        self.max_count = self.employees.count()

        # Generate payslips
        self.generate()

    def load_excel(self, obj):
        """
        Load Excel file into a DataFrame, fill NaN with 0, and convert the first column to string.
        """
        # Load DataFrame from Excel if path exists, otherwise create an empty DataFrame
        df = pd.DataFrame()
        if obj and obj.url:
            df = pd.read_excel(obj.url, dtype={field:str for field in self.string_fields}, sheet_name=None)
            df = pd.concat(df.values())

        # Fill NaN values with 0
        df.fillna(0, inplace=True)
        
        # Check if DataFrame is not empty
        if not df.empty:
            # Get the name of the first column
            first_column = df.columns[0]

            # Convert the first column to string
            df[first_column] = df[first_column].astype(str)
        
        # Return the DataFrame
        return df
    
    def _get_df_row_from_column_value(self, df, column, value):
        if df.empty or column not in df.columns: return pd.DataFrame()
        return df.loc[df[column] == value]
    
    def df_column_sum(self, df, columns):
        if not all(col in df.columns for col in columns): return 0
        return df.apply(lambda row: sum(row[col] for col in columns), axis=1).sum()
    
    def get_canvas_of(self, registration_number):
        return self._get_df_row_from_column_value(self.canvas, 'registration_number', registration_number)

    def queryset_iterator(self, queryset, chunk_size=100):
        """
        Iterate over a Django Queryset in chunks using itertools.islice.
        """
        offset, total_count = 0, queryset.count()

        while offset < total_count:
            chunk = queryset[offset:offset + chunk_size]
            if not chunk: break
            yield list(chunk)
            offset += chunk_size

    def process_chunk(self, employees):
        for employee in employees:
            payslip = self.create_payslip(employee)

            # calculate items for the employee
            self.generate_items(self.items, payslip, employee)

            # calculate special items of the employee
            _items = employee.specialemployeeitem_set.filter(
                Q(end_date__isnull=True) | Q(end_date__gte=self.payroll.end_dt),
            ).select_related('item')
            self.generate_items(_items, payslip, employee, condition=False)

            payslip = self.refresh_payslip(payslip)
            
            self.insert_items_from_df(self.additional_items, payslip, employee)
            payslip = self.refresh_payslip(payslip)
            
            self.generate_items(self.legal_items, payslip, employee)
            payslip = self.refresh_payslip(payslip)
        
    def generate(self):
        """
        Generate payslips for all filtered employees.
        """
        try:
            # split the process into multiple parallel process
            chunks = self.queryset_iterator(self.employees, self.chunks_size)

            # Using ThreadPoolExecutor for multi-threading
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                # Submit all tasks to the thread pool
                future_to_chunk = {executor.submit(self.process_chunk, chunk): chunk for chunk in chunks}

                # Wait for all threads to complete and collect results
                for future in as_completed(future_to_chunk):
                    future.result()

            self.payroll = self.refresh_payroll(status=PayrollStatus.SUCCESS)
            Notification.objects.get_or_create(**{
                '_from': self.payroll.created_by,
                '_to': self.payroll.created_by,
                'message': 'La paie a été générée avec succès.',
                'subject': f"Paie #{self.payroll.name}",
                'redirect': self.payroll.get_absolute_url()
            })
        except Exception as ex:
            self.handle_generation_exception(ex)

    def handle_generation_exception(self, ex):
        """
        Handle exceptions during payslip generation.
        """
        self.payroll._metadata.setdefault('errors', []).append({'message': str(ex), 'tag': 'error'})
        Notification.objects.get_or_create(**{
            '_from': self.payroll.created_by,
            '_to': self.payroll.created_by,
            'message': str(ex),
            'subject': f"Erreur paie #{self.payroll.name}",
            'redirect': self.payroll.get_absolute_url()
        })
        Payroll.objects.filter(pk=self.payroll.pk).update(**{'status': PayrollStatus.WARNING, '_metadata': self.payroll._metadata})
        self.payroll.refresh_from_db()

    def evaluate_formulas(self, item, employee, payslip, canvas, items_paid=[]):
        """
        Safely evaluate the formulas for employee and employer.
        """
        try:
            working_days_per_month = getattr(employee, 'working_days_per_month', 30)
            time = float(eval(item.time, locals()) or 0) if hasattr(item, 'time') else 0
            formula_qp_employee = abs(round(eval(item.formula_qp_employee, locals()), 2)) * item.type_of_item
            formula_qp_employer = abs(round(eval(item.formula_qp_employer, locals()), 2)) * item.type_of_item
            return time, formula_qp_employee, formula_qp_employer
        except Exception as ex:
            self.errors.append({'message': str(ex), 'tag': 'error'})
            # return 0, 0, 0

    def create_payslip(self, employee):
        """
        Create payslip for the employee.
        """

        data = employee.__dict__.items()
        data = {k: v for k, v in data if k not in ['_state', 'id', 'photo', 'user_id', 'email']}

        employee = PaidEmployee(**data, payroll=self.payroll)
        employee.save()
        
        return Payslip.objects.create(**{
            'employee': employee,
            'payroll': self.payroll,
            'created_by': self.payroll.created_by
        })

    def refresh_payslip(self, payslip):
        items_paid = payslip.itempaid_set.filter(is_payable=True)
        
        social_security_amount = round(items_paid.aggregate(amount=Sum('social_security_amount'))['amount'] or 0, 2)
        amount_qp_employee = round(items_paid.aggregate(amount=Sum('amount_qp_employee'))['amount'] or 0, 2)
        taxable_amount = round(items_paid.aggregate(amount=Sum('taxable_amount'))['amount'] or 0, 2)

        Payslip.objects.filter(pk=payslip.pk).update(**{
            'social_security_threshold': social_security_amount,
            'taxable_gross': taxable_amount,
            'gross': amount_qp_employee,
            'net': amount_qp_employee
        })

        return Payslip.objects.get(pk=payslip.pk)
    
    def refresh_payroll(self, status=None):
        """
        Update the payroll status and overall net amount.
        """
        net = self.payroll.payslip_set.aggregate(amount=Sum('net')).get('amount', 0)
        net = round(net, 2) if net else 0

        Payroll.objects.filter(pk=self.payroll.pk).update(**{
            'overall_net': net, 
            'status': status if status else self.payroll.status
        })
        return Payroll.objects.get(pk=self.payroll.pk)

    def generate_items(self, items, payslip, employee, condition=True):
        """
        - items (QuerySet or list): The items to process.
        - payslip (Payslip): The payslip instance.
        - employee (Employee): The employee instance.
        - condition (bool, optional): A condition to evaluate for each item. Defaults to True.
        list: A list of created `ItemPaid` instances.
        Raises:
        Exception: If an error occurs during item processing, an exception is raised with details.
        
        Generate or update items for a payslip and employee.
        
        Parameters:
        - items: QuerySet or list of items to process.
        - payslip: The payslip instance.
        - employee: The employee instance.
        
        Returns:
        A list of created `ItemPaid` instances.
        """
        item_to_pay_queryset = []
        for item in items:
            canvas = None
            amount_qp_employee, amount_qp_employer = 0, 0
            if isinstance(item, SpecialEmployeeItem):
                amount_qp_employee, amount_qp_employer, item = item.amount_qp_employee, item.amount_qp_employer, item.item
            try:
                if condition:
                    canvas = self.get_canvas_of(employee.registration_number)
                    if not eval(item.condition, locals()): continue
                
                time, qpe, qpp = (0, amount_qp_employee, amount_qp_employer)
                if not any([qpe, qpp]):
                    time, qpe, qpp = self.evaluate_formulas(item, employee, payslip, canvas, item_to_pay_queryset)
                
                if int(qpe) == 0 and int(qpp) == 0: continue
                item_to_pay_queryset.append(ItemPaid(
                    code=item.code,
                    type_of_item=item.type_of_item,
                    name=item.name, time=time, rate=round(qpe/time, 2) if time else 0,
                    amount_qp_employer=qpp, amount_qp_employee=qpe,
                    taxable_amount=qpe if getattr(item, 'is_taxable', False) else 0,
                    social_security_amount=qpe if getattr(item, 'is_social_security', False) else 0,
                    is_bonus=getattr(item, 'is_bonus', False), is_payable=getattr(item, 'is_payable', True),
                    payslip=payslip, created_by=self.payroll.created_by
                ))
            except Exception as ex:
                self.errors.append({'message': str(ex), 'tag': 'error'})
                message = {
                    'item': item.code,
                    'item.name': item.name,
                    'employee': employee.registration_number,
                }
                message = [f"{k}:{v} \n " for k,v in message.items()]
                raise Exception(str(ex)+" \n ".join(message))
        return ItemPaid.objects.bulk_create(item_to_pay_queryset)

    def re_base_additional_element_column(self, df):
        columns = {
            'matricule': 'matricule',
            'type d\'element': 'type_of_item',
            'code': 'code',
            'nom': 'name',
            'temps': 'time',
            'taux': 'rate',
            'montant quote part employee': 'amount_qp_employee',
            'montant quote part employeur': 'amount_qp_employer',
            'plafond de la sécurité sociale': 'social_security_amount',
            'montant imposable': 'taxable_amount',
            'est une prime': 'is_bonus',
            'est payable': 'is_payable'
        }

        df.columns = [columns.get(col, col) for col in df.columns]
        float_columns = ['time', 'rate', 'amount_qp_employee', 'amount_qp_employer', 'social_security_amount', 'taxable_amount']

        for column in float_columns:
            df[column] = df[column].astype(float).fillna(0)
        return df

    def insert_items_from_df(self, df, payslip, employee):
        if df.empty: return
        df = df[df['matricule'] == employee.registration_number]

        df['is_payable'] = df['is_payable'].replace({'TRUE': True, 'FALSE': False})
        df['is_bonus'] = df['is_bonus'].replace({'TRUE': True, 'FALSE': False})

        df.pop('matricule')

        data = json.loads(df.to_json(orient='records'))
        data = [ItemPaid(**obj, payslip=payslip) for obj in data]
        return ItemPaid.objects.bulk_create(data)

app.register_task(Payer())