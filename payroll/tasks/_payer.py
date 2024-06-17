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

        # replace all the nan to 0 and convert the key column to type str
        for k, df in [('registration_number', self.canvas),('matricule', self.additional_items)]:
            df.fillna(0, inplace=True)
            df[k] = df[k].astype(str)

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

    def load_excel(self, path):
        """
        Load Excel file into a DataFrame.
        """
        path = path.path if path else None
        return pd.read_excel(path) if path else pd.DataFrame()
    
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
                self.generate_items(self.legal_items, payslip, employee)
                payslip = self.refresh_payslip(payslip)
            self.refresh_payroll(status=PayrollStatus.SUCCESS)
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
            time = eval(item.time, locals()) or item.time or 0
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

        payslip.refresh_from_db()
        return payslip
    
    def refresh_payroll(self, status=None):
        """
        Update the payroll status and overall net amount.
        """
        net = self.payroll.payslip_set.aggregate(amount=Sum('net')).get('amount', 0)
        net = round(net, 2) if net else 0

        Payroll.objects.filter(pk=self.payroll.pk).update(**{'overall_net': net, 'status': self.payroll.status if status else self.payroll.status})

        self.payroll.refresh_from_db()
        return self.payroll

    def generate_items(self, items, payslip, employee):
        itempaid = payslip.itempaid_set.all().values_list('code', flat=True)
        item_to_pay = []

        for item in items:
            if item.code in itempaid: continue
            if not eval(item.condition, locals()): continue
            time, qpe, qpp = self.evaluate_formulas(item, employee, payslip)
            item_to_pay.append(ItemPaid(
                code=item.code,
                type_of_item=item.type_of_item,
                name=item.name, time=time, rate=round(qpe/time, 2) if time else 0,
                amount_qp_employer=qpp, amount_qp_employee=qpe,
                taxable_amount=qpe if item.is_taxable else 0,
                social_security_amount=qpe if item.is_social_security else 0,
                is_bonus=item.is_bonus, is_payable=item.is_payable,
                payslip=payslip, created_by=self.payroll.created_by
            ))
        return ItemPaid.objects.bulk_create(item_to_pay)

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