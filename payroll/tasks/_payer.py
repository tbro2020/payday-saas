from employee.models import Employee, MaritalStatus
from django.db.models import Sum, Q
from django.db import transaction

from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from payroll.models import *
from celery import Task
import pandas as pd

from api.serializers import model_serializer_factory
from datetime import datetime
from payday.celery import app

# Serializer for Employee model
EmployeeSerializer = model_serializer_factory(Employee)

class Payer(Task):
    """
    Celery Task to handle payroll processing and payslip generation.
    """
    errors = []
    name = 'payer'
    ignore_result = True        

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
        self.today = datetime.now()
        self.payroll = get_object_or_404(Payroll, pk=pk)

        # Load additional items from Excel
        self.canvas = self.load_excel(self.payroll.canvas)
        self.additional_items = self.load_excel(self.payroll.additional_items)

        self.legal_items = LegalItem.objects.all()
        self.items = Item.objects.filter(is_payable=True)
        self.items = self.items.exclude(Q(condition='0') | Q(condition__isnull=True))

        # Build and apply employee filter
        self.employees = Employee.objects.select_related().all()
        self.employees = self.employees.filter(**{
            k:v for k, v in {
                'grade__in': self.payroll.employee_grade.values_list('id', flat=True),
                'branch__in': self.payroll.employee_branch.values_list('id', flat=True),
                'status__in': self.payroll.employee_status.values_list('id', flat=True),
                'direction__in': self.payroll.employee_direction.values_list('id', flat=True)
            }.items() if v
        }).filter(**kwargs.get('employee', {}))

        # Generate payslips
        self.generate()

    def load_excel(self, obj):
        """
        Load Excel file into a DataFrame, fill NaN with 0, and convert the first column to string.
        """
        # Load DataFrame from Excel if path exists, otherwise create an empty DataFrame
        df = pd.read_excel(obj.path) if obj and obj.path else pd.DataFrame()
        
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
    
    @transaction.atomic
    def generate(self):
        """
        Generate payslips for all filtered employees.
        """
        try:
            for employee in self.employees:
                payslip, created = self.create_or_get_payslip(employee)
                self.generate_items(self.items, payslip, employee)
                payslip = self.refresh_payslip(payslip)
                self.generate_items(self.legal_items, payslip, employee, can_delete_existing_item_paid=True)
                payslip = self.refresh_payslip(payslip)
            self.payroll = self.refresh_payroll(status=PayrollStatus.SUCCESS)
        except Exception as ex:
            self.handle_generation_exception(ex)

    def handle_generation_exception(self, ex):
        """
        Handle exceptions during payslip generation.
        """
        self.payroll.metadata.setdefault('errors', []).append({'message': str(ex), 'tag': 'error'})
        self.payroll.created_by.email_user(_(f"Erreur paie #{self.payroll.name}"), str(ex))
        
        Payroll.objects.filter(pk=self.payroll.pk).update(**{'status': PayrollStatus.WARNING, 'metadata': self.payroll.metadata})
        self.payroll.refresh_from_db()

    def evaluate_formulas(self, item, employee, payslip):
        """
        Safely evaluate the formulas for employee and employer.
        """
        try:
            time = float(eval(item.time, locals()) or 0)
            formula_qp_employee = abs(round(eval(item.formula_qp_employee, locals()), 2)) * item.type_of_item
            formula_qp_employer = abs(round(eval(item.formula_qp_employer, locals()), 2)) * item.type_of_item
            return time, formula_qp_employee, formula_qp_employer
        except Exception as ex:
            return 0, 0, 0

    def create_or_get_payslip(self, employee):
        """
        Create or get an existing payslip for the employee.
        """
        emp = EmployeeSerializer(employee).data
        return Payslip.objects.get_or_create(_employee=emp, payroll=self.payroll, created_by=self.payroll.created_by)

    def refresh_payslip(self, payslip):
        items_paid = payslip.itempaid_set.filter(is_payable=True)
        
        social_security_amount = round(items_paid.aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        amount_qp_employee = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        taxable_amount = round(items_paid.aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)

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

        Payroll.objects.filter(pk=self.payroll.pk).update(**{'overall_net': net, 'status': self.payroll.status if status else self.payroll.status})
        return Payroll.objects.get(pk=self.payroll.pk)

    def generate_items(self, items, payslip, employee, can_delete_existing_item_paid=False):
        """
        Generate or update items for a payslip and employee.
        
        Parameters:
        - items: QuerySet or list of items to process.
        - payslip: The payslip instance.
        - employee: The employee instance.
        - can_delete_existing_item_paid: Flag to indicate if existing paid items should be deleted.
        
        Returns:
        A list of created `ItemPaid` instances.
        """
        item_to_pay_queryset = []
        item_paid_queryset = payslip.itempaid_set.all()
        
        if can_delete_existing_item_paid:
            # Delete existing item paid records that match the codes in items
            item_paid_queryset.filter(code__in=items.values_list('code', flat=True))._raw_delete(item_paid_queryset.db)
            item_paid_codes = set(payslip.itempaid_set.all().values_list('code', flat=True))
        else:
            # Get existing paid item codes
            item_paid_codes = set(item_paid_queryset.values_list('code', flat=True))

        for item in items:
            if item.code in item_paid_codes: continue
            if not eval(item.condition, locals()): continue
            time, qpe, qpp = self.evaluate_formulas(item, employee, payslip)
            # if int(qpe) == 0 and int(qpp) == 0: continue
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
        return ItemPaid.objects.bulk_create(item_to_pay_queryset)

    def get_tranche(self, taxable_gross):
        for percentage, (lower_bound, upper_bound) in self.TRANCHES.items():
            if lower_bound <= taxable_gross <= upper_bound:
                return {'percentage': percentage, 'tranche': (lower_bound, upper_bound)}
        return None

    def calculate_tax(self, payslip, employee, **kwargs):
        taxable_amount = payslip.taxable_gross - (payslip.social_security_threshold * kwargs.get('cnss', 0.05))
        tranche = self.get_tranche(taxable_amount)
        
        if not tranche:
            raise ValueError("Taxable amount does not fall within any tranches.")
        
        taxable_amount -= tranche['tranche'][0]
        taxable_amount *= tranche['percentage']
        taxable_amount += 4860
        
        person_count = int(payslip.employee.metadata.get('NOMBRE_ENFANT', 0))
        person_count = person_count if person_count > 0 or employee is None else employee.child_set.count()
        person_count += 1 if payslip.employee.marital_status == MaritalStatus.Married else 0

        charge = taxable_amount * (0.02 * person_count)
        taxable_amount -= charge
        return round(taxable_amount, 2)

app.register_task(Payer())