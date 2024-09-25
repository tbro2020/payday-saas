from concurrent.futures import ThreadPoolExecutor, as_completed
from employee import models as employee_model
from django.db.models import Sum, Q
from django.conf import settings
import os

from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from payroll import models as payroll_model
from celery import Task
import pandas as pd

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

    baremes = {
        remove_leading_zero(grade['name']): grade['metadata']
        for grade in employee_model.Grade.objects.values('name', 'metadata')
    }     

    TRANCHES = {
        0.03: [0, 162000],
        0.15: [162001, 1800000],
        0.30: [1800001, 3600000],
        0.40: [3600001, 9999999999999]
    }

    def run(self, pk, *args, **kwargs):
        """
        Main entry point for the task. Processes the payroll.
        """
        DEBUG = settings.DEBUG
        self.now = datetime.now()
        self.today = self.now.today
        self.chunks_size = int(getattr(settings, 'PAYROLL_CHUNCKS_SIZE', 100))
        
        self.workers = os.cpu_count() * (1.0 if DEBUG else 1.5)
        self.payroll = get_object_or_404(payroll_model.Payroll, pk=pk)

        # Load additional items from Excel
        self.canvas = self.load_excel(self.payroll.canvas)
        self.additional_items = self.load_excel(self.payroll.additional_items)
        if not self.additional_items.empty:
            self.additional_items = self.re_base_additional_element_column(self.additional_items)
        
        self.legal_items = payroll_model.LegalItem.objects.all()
        self.items = payroll_model.Item.objects.exclude(Q(condition='0') | Q(condition__isnull=True)).order_by('code')

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
            df = pd.read_excel(obj.url, dtype={'matricule': str, 'registration_number': str}, sheet_name=None)
            
            # Concatenate all DataFrames into one
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
            _items = employee.specialemployeeitem_set.all().select_related('item')
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

            self.payroll = self.refresh_payroll(status=payroll_model.PayrollStatus.SUCCESS)
            # self.update_task_state(is_last=True, meta={'current': self.employees.count(), 'total': self.employees.count()})
        except Exception as ex:
            #self.update_task_state(s_last=True, meta={'current': 0, 'total': self.employees.count()})
            self.handle_generation_exception(ex)

    def handle_generation_exception(self, ex):
        """
        Handle exceptions during payslip generation.
        """
        self.payroll.metadata.setdefault('errors', []).append({'message': str(ex), 'tag': 'error'})
        self.payroll.created_by.email_user(_(f"Erreur paie #{self.payroll.name}"), str(ex))
        
        payroll_model.Payroll.objects.filter(pk=self.payroll.pk).update(**{'status': payroll_model.PayrollStatus.WARNING, 'metadata': self.payroll.metadata})
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
        data = {k: v for k, v in data if k not in ['_state', 'id']}

        emp = payroll_model.Employee(**data, payroll=self.payroll)
        emp.save()
        
        return payroll_model.Payslip.objects.create(**{
            'employee': emp,
            'payroll': self.payroll,
            'created_by': self.payroll.created_by
        })

    def refresh_payslip(self, payslip):
        items_paid = payslip.itempaid_set.filter(is_payable=True)
        
        social_security_amount = round(items_paid.aggregate(amount=Sum('social_security_amount'))['amount'] or 0, 2)
        amount_qp_employee = round(items_paid.aggregate(amount=Sum('amount_qp_employee'))['amount'] or 0, 2)
        taxable_amount = round(items_paid.aggregate(amount=Sum('taxable_amount'))['amount'] or 0, 2)

        payroll_model.Payslip.objects.filter(pk=payslip.pk).update(**{
            'social_security_threshold': social_security_amount,
            'taxable_gross': taxable_amount,
            'gross': amount_qp_employee,
            'net': amount_qp_employee
        })

        return payroll_model.Payslip.objects.get(pk=payslip.pk)
    
    def refresh_payroll(self, status=None):
        """
        Update the payroll status and overall net amount.
        """
        net = self.payroll.payslip_set.aggregate(amount=Sum('net')).get('amount', 0)
        net = round(net, 2) if net else 0

        payroll_model.Payroll.objects.filter(pk=self.payroll.pk).update(**{'overall_net': net, 'status': status if status else self.payroll.status})
        return payroll_model.Payroll.objects.get(pk=self.payroll.pk)

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
            if isinstance(item, payroll_model.SpecialEmployeeItem):
                amount_qp_employee, amount_qp_employer, item = item.amount_qp_employee, item.amount_qp_employer, item.item
            try:
                if condition:
                    canvas = self.get_canvas_of(employee.registration_number)
                    if not eval(item.condition, locals()): continue
                
                time, qpe, qpp = (0, amount_qp_employee, amount_qp_employer)
                if not any([amount_qp_employee, amount_qp_employer]):
                    time, qpe, qpp = self.evaluate_formulas(item, employee, payslip, canvas, item_to_pay_queryset)
                
                if int(qpe) == 0 and int(qpp) == 0: continue
                item_to_pay_queryset.append(payroll_model.ItemPaid(
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
        return payroll_model.ItemPaid.objects.bulk_create(item_to_pay_queryset)

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
        data = [payroll_model.ItemPaid(**obj, payslip=payslip) for obj in data]
        return payroll_model.ItemPaid.objects.bulk_create(data)

    def get_tranche(self, taxable_gross):
        for percentage, (lower_bound, upper_bound) in self.TRANCHES.items():
            if lower_bound <= taxable_gross <= upper_bound:
                return {'percentage': percentage, 'tranche': (lower_bound, upper_bound)}
        return None

    def calculate_tax(self, payslip, employee, **kwargs):
        items = payslip.itempaid_set.filter(is_payable=True)
        not_bonus = items.filter(is_bonus=False)

        social_security_threshold = not_bonus.aggregate(amount=Sum('social_security_amount'))['amount'] or 0
        taxable_gross = not_bonus.aggregate(amount=Sum('taxable_amount'))['amount'] or 0

        taxable_amount = taxable_gross - (social_security_threshold * kwargs.get('cnss', 0.05))
        tranche = self.get_tranche(taxable_amount)
        
        if not tranche:
            raise ValueError("Taxable amount does not fall within any tranches.")
        
        taxable_amount -= tranche['tranche'][0]
        taxable_amount *= tranche['percentage']
        taxable_amount += 4860

        bonus = items.filter(is_bonus=True).aggregate(amount=Sum('taxable_amount'))['amount'] or 0
        bonus = bonus*0.03

        taxable_amount = taxable_amount + bonus

        person_count = int(payslip.employee.metadata.get('NOMBRE_ENFANT', 0)) if 'NOMBRE_ENFANT' in payslip.employee.metadata else 0
        person_count = person_count if person_count > 0 or employee is None else employee.child_set.count()
        person_count += 1 if payslip.employee.marital_status == 'married' else 0

        charge = taxable_amount * (0.02 * person_count)
        taxable_amount -= charge

        return round(taxable_amount, 2)

    def shift(self, item, payslip, employee):
        if self.canvas.empty: return
        HEURE_MAJOREES = item.metadata['HEURE_MAJOREES'] or {}
        period = "0" + self.payroll.start_dt.month.replace('0','')

        data = self.canvas[self.canvas['MATRICULE'] == employee.registration_number]
        data = data[data['MOIS_EFFET'] == period]
        data = data.to_json(orient='records')

        hours = 0
        for obj in data:
            days = int(obj['NOMBRE_JOURS'])
            code_activites = str(obj['CODE_ABSENCE'])
            hours += (HEURE_MAJOREES[code_activites.lower()] or 0) * days
        
        items_paid = payslip.itempaid_set.filter(code__in=['1010','1000','3800','3260','3620','3640'])
        items_paid = items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0)
        result = items_paid / 195
        result = result * hours
        result = result * 1.1818

app.register_task(Payer())