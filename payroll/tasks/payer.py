from employee.models import Employee, MaritalStatus
from django.db.models import Sum, Q

from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from payroll.models import LegalItem, Item, ItemPaid, Payslip, PayrollStatus
from celery import Task

from django.apps import apps
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

    def __init__(self):
        # Pre-fetch legal items and payable items to avoid repeated queries
        self.today = datetime.now()
        self.legal_items = LegalItem.objects.all()
        self.employees = Employee.objects.select_related().all()
        self.items = Item.objects.filter(is_payable=True).exclude(Q(condition='0') | Q(condition__isnull=True))

    def run(self, payroll_id, *args, **kwargs):
        """
        Main entry point for the task. Processes the payroll.
        """
        Payroll = apps.get_model('payroll', 'Payroll')
        self.payroll = get_object_or_404(Payroll, pk=payroll_id)

        # Load additional items from Excel
        self.canvas = self.load_excel(self.payroll.canvas)
        self.additional_items = self.load_excel(self.payroll.additional_items)

        if not self.additional_items.empty:
            self.additional_items.fillna(0, inplace=True)
            self.additional_items['matricule'] = self.additional_items['matricule'].astype(str)

        # Build and apply employee filter
        payroll_employee_filter = self.build_payroll_employee_filter()
        self.employees = self.filter_employees(payroll_employee_filter)

        # Generate payslips
        self.generate()

    def load_excel(self, path):
        """
        Load Excel file into a DataFrame.
        """
        path = path.path if path else None
        return pd.read_excel(path) if path else pd.DataFrame()

    def build_payroll_employee_filter(self):
        """
        Build a dictionary of filters for selecting employees based on payroll criteria.
        """
        return {
            k:v
            for k, v in {
                'grade__in': self.payroll.employee_grade.values_list('id', flat=True),
                'branch__in': self.payroll.employee_branch.values_list('id', flat=True),
                'status__in': self.payroll.employee_status.values_list('id', flat=True),
                'direction__in': self.payroll.employee_direction.values_list('id', flat=True)
            }.items() if v
        }

    def filter_employees(self, payroll_employee_filter):
        """
        Filter employees based on the provided filters.
        """
        return self.employees.filter(**payroll_employee_filter)

    def generate(self, *args, **kwargs):
        """
        Generate payslips for all filtered employees.
        """
        try:
            for employee in self.employees:
                payslip = self.create_or_get_payslip(employee)
                self.process_payslip_items(payslip, employee)
            self.update_payroll_status(PayrollStatus.SUCCESS)
        except Exception as ex:
            self.handle_generation_exception(ex)

    def create_or_get_payslip(self, employee):
        """
        Create or get an existing payslip for the employee.
        """
        return Payslip.objects.get_or_create(
            _employee=EmployeeSerializer(employee).data,
            payroll=self.payroll,
            created_by=self.payroll.created_by
        )[0]

    def process_payslip_items(self, payslip, employee):
        """
        Process and calculate the payable items for the payslip.
        """
        items_to_pay = self.calculate_items_to_pay(payslip, employee)
        self.bulk_create_items(items_to_pay)
        self.finalize_payslip(payslip)
        self.process_legal_items(payslip, employee)
        
    def calculate_items_to_pay(self, payslip, employee):
        """
        Calculate the items to be paid on the payslip.
        """
        items_to_pay = []
        items_paid_code = payslip.itempaid_set.values_list('code', flat=True)

        for item in self.items:
            if item.code in items_paid_code:
                continue

            if not self.evaluate_condition(item.condition, employee):
                continue

            formula_qp_employee, formula_qp_employer = self.evaluate_formulas(item, employee)
            if formula_qp_employee == 0 and formula_qp_employer:
                continue

            rate = self.calculate_rate(formula_qp_employee, item, employee)
            items_to_pay.append(self.create_item_paid(item, payslip, rate, formula_qp_employee, formula_qp_employer))

        if not self.additional_items.empty:
            additional_items = self.process_additional_items(payslip, employee)
            items_to_pay.extend(additional_items)

        return items_to_pay

    def evaluate_condition(self, condition, employee):
        """
        Safely evaluate the condition for an item.
        """
        try:
            return eval(condition, locals())
        except Exception:
            return False

    def evaluate_formulas(self, item, employee, payslip=None):
        """
        Safely evaluate the formulas for employee and employer.
        """
        try:
            time = eval(item.time, locals()) or item.time
            formula_qp_employee = abs(round(eval(item.formula_qp_employee, locals()), 2)) * item.type_of_item
            formula_qp_employer = abs(round(eval(item.formula_qp_employer, locals()), 2)) * item.type_of_item
            return formula_qp_employee, formula_qp_employer
        except Exception as ex:
            return 0, 0

    def calculate_rate(self, formula_qp_employee, item, employee):
        """
        Calculate the rate for an item.
        """
        try:
            time = eval(item.time, locals())
            return round(abs(formula_qp_employee / time) if time > 0 else abs(formula_qp_employee), 2)
        except Exception:
            return 0

    def create_item_paid(self, item, payslip, rate, formula_qp_employee, formula_qp_employer):
        """
        Create an ItemPaid instance.
        """
        return ItemPaid(
            code=item.code,
            type_of_item=item.type_of_item,
            name=item.name,
            time=rate,
            rate=rate,
            amount_qp_employer=formula_qp_employer,
            amount_qp_employee=formula_qp_employee,
            taxable_amount=formula_qp_employee if item.is_taxable else 0,
            social_security_amount=formula_qp_employee if item.is_social_security else 0,
            is_bonus=item.is_bonus,
            is_payable=item.is_payable,
            payslip=payslip,
            created_by=self.payroll.created_by
        )

    def process_additional_items(self, payslip, employee):
        """
        Process additional items from the additional items DataFrame.
        """
        df = self.additional_items[self.additional_items['matricule'] == employee.registration_number]
        if df.empty: return []
        return [
            ItemPaid(
                code=item.get('code'),
                name=item.get('nom'),
                type_of_item=item.get("type d'element", 1),
                time=item.get('temps', 0),
                rate=item.get('taux', 0),
                amount_qp_employer=item.get('montant quote part employeur'),
                amount_qp_employee=item.get('montant quote part employee'),
                taxable_amount=item.get('montant imposable'),
                social_security_amount=item.get('plafond de la sécurité sociale'),
                is_bonus=item.get('est une prime', False),
                is_payable=item.get('est payable', False),
                payslip=payslip,
                created_by=self.payroll.created_by
            )
            for item in df.to_dict(orient='records')
        ]

    def bulk_create_items(self, items_to_pay):
        """
        Bulk create ItemPaid instances.
        """
        ItemPaid.objects.bulk_create(items_to_pay)

    def finalize_payslip(self, payslip):
        """
        Finalize and save the payslip with calculated totals.
        """
        items_paid = payslip.itempaid_set.filter(is_payable=True)

        payslip.gross = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.net = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.social_security_threshold = round(items_paid.aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        payslip.taxable_gross = round(items_paid.aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.save()

    def update_payroll_status(self, status):
        """
        Update the payroll status and overall net amount.
        """
        overall_net = self.payroll.payslip_set.aggregate(amount=Sum('net')).get('amount', 0)
        self.payroll.overall_net = round(overall_net, 2) if overall_net else 0
        self.payroll.status = status
        self.payroll.save()

    def handle_generation_exception(self, ex):
        """
        Handle exceptions during payslip generation.
        """
        self.payroll.status = PayrollStatus.WARNING
        self.payroll.metadata.setdefault('errors', []).append({'message': str(ex), 'tag': 'error'})
        self.payroll.created_by.email_user(
            _(f"Il semble que quelque chose n'a pas fonctionné dans votre système de paie {self.payroll.name}"), str(ex)
        )
        self.payroll.save()

    def process_legal_items(self, payslip, employee):
        """
        Process legal items for the payslip.
        """
        legal_items_to_pay = self.calculate_legal_items(payslip, employee)
        self.bulk_create_items(legal_items_to_pay)
        self.finalize_payslip(payslip)

    def calculate_legal_items(self, payslip, employee):
        """
        Calculate the legal items for the payslip.
        """
        legal_items_to_pay = []
        qs = payslip.itempaid_set.filter(code__in=self.legal_items.values_list('code', flat=True))
        qs._raw_delete(qs.db)

        for legal in self.legal_items:
            if not self.evaluate_condition(legal.condition, locals()):
                continue

            formula_qp_employee, formula_qp_employer = self.evaluate_formulas(legal, employee, payslip)
            legal_items_to_pay.append(self.create_legal_item_paid(legal, payslip, formula_qp_employee, formula_qp_employer))

        return legal_items_to_pay
    
    def tax(self, payslip, employee, **kwargs):
        tranches = {
            0.03: [0, 162000],
            0.15: [162001, 1800000],
            0.30: [1800001, 3600000],
            0.40: [3600001, 9999999999999]
        }
        ipr = payslip.taxable_gross - (payslip.social_security_threshold * kwargs.get('cnss', 0.05))
        tranche = next({'percentage': key, 'tranche': value} for key, value in tranches.items() if value[0] <= ipr <= value[-1])
        
        ipr = ipr - tranche.get('tranche')[0]
        ipr = ipr * tranche.get('percentage')
        ipr = ipr + 4860
        
        person = int(payslip.employee.metadata.get('NOMBRE_ENFANT', 0))
        person = person if person > 0 or employee == None else employee.child_set.count()
        person = person + (1 if payslip.employee.marital_status == MaritalStatus.Maried.value else 0)

        charge = 0.02*person
        charge = ipr*charge
        ipr = ipr - charge
        return round(ipr, 2)

    def create_legal_item_paid(self, legal, payslip, formula_qp_employee, formula_qp_employer):
        """
        Create an ItemPaid instance for a legal item.
        """
        return ItemPaid(
            code=legal.code,
            name=legal.name,
            time=0,
            rate=0,
            type_of_item=legal.type_of_item,
            amount_qp_employer=formula_qp_employer,
            amount_qp_employee=formula_qp_employee,
            payslip=payslip,
            created_by=self.payroll.created_by
        )


app.register_task(Payer())