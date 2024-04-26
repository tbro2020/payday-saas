from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from employee.models import Employee
from django.db.models import Sum
from payroll.models import *
from celery import Task

from payday.celery import app

class Payer(Task):
    errors = []
    name = 'payer'
    ignore_result = True

    legal_items = LegalItem.objects.all()
    items = Item.objects.filter(is_payable=True)
    employees = Employee.objects.select_related().all()

    def run(self, payroll, *args, **kwargs):
        self.payroll = get_object_or_404(Payroll, pk=payroll)
        
        payroll_employee_filter = {
            'grade__in': self.payroll.employee_grade.all(),
            'status__in': self.payroll.employee_status.all(),
            'branch__in': self.payroll.employee_branch.all(),
            'direction__in': self.payroll.employee_direction.all()
        }
        
        self.employees = self.employees.filter(**{key:value for key, value in payroll_employee_filter.items() if value})
        self.generate()

    def generate(self, *args, **kwargs):
        try:
            for employee in self.employees:
                payslip = self._payslip(employee)
                self._duty(payslip)
            overall_net = self.payroll.payslip_set.all().aggregate(amount=Sum('net')).get('amount', 0)
            self.payroll.overall_net = round(overall_net, 2) if overall_net else 0
            self.payroll.status = PayrollStatus.SUCCESS
            self.payroll.save()
            # send email that the payroll is done

        except Exception as ex:
            self.payroll.status = PayrollStatus.WARNING
            self.payroll.metadata['errors'].append({'message': str(ex), 'tag': 'error'})
            self.payroll.created_by.email_user(_(f"Il semble que quelque chose n'a pas fonctionné dans votre système de paie {self.payroll.name}"), str(ex))
            self.payroll.save()
            # generate error

    def _payslip(self, employee: Employee):
        pay_items = []
        payslip, created = Payslip.objects.get_or_create(employee=employee, payroll=self.payroll)

        for item in self.items:
            condition = eval(item.condition, locals())
            if not condition: continue
            time = eval(item.time, locals())

            # formula qp employee
            formula_qp_employee = round(eval(item.formula_qp_employee, locals()), 2)
            formula_qp_employee = abs(formula_qp_employee) * item.type_of_item

            # formula qp employer
            formula_qp_employer = round(eval(item.formula_qp_employer, locals()), 2)
            formula_qp_employer = abs(formula_qp_employer) * item.type_of_item

            if formula_qp_employee == 0 and formula_qp_employer: continue

            rate = (formula_qp_employee / time) if time > 0 else formula_qp_employee
            rate = round(abs(rate), 2)

            # Generate item paid
            pay_item: ItemPaid = ItemPaid.objects.create(
                **{'code': item.code, 
                    'type_of_item': item.type_of_item, 

                    'name': item.name, 
                    'time': time, 
                    'rate': rate,

                    'amount_qp_employer': formula_qp_employer, 
                    'amount_qp_employee': formula_qp_employee, 

                    'taxable_amount': formula_qp_employee if item.is_taxable else 0,
                    'social_security_amount': formula_qp_employee if item.is_social_security else 0,
                    
                    'payslip': payslip})
            pay_items.append(pay_item)

        if not created:
            payslip.itempaid_set.filter(code__in=[item.code for item in pay_items]).delete()

        # Calculate the fixed value
        payslip.net = round(payslip.itempaid_set.all().aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.gross = round(payslip.itempaid_set.all().aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)

        payslip.taxable_gross = round(payslip.itempaid_set.all().aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.social_security_threshold = round(payslip.itempaid_set.all().aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        payslip.save()

        return payslip

    def _duty(self, payslip: Payslip):
        pay_items = []

        for legal in self.legal_items:
            condition = eval(legal.condition, locals())
            if not condition: continue

            # formula qp employee
            formula_qp_employee = round(eval(legal.formula_qp_employee, locals()), 2)
            formula_qp_employee = abs(formula_qp_employee) * legal.type_of_item

            # formula qp employer
            formula_qp_employer = round(eval(legal.formula_qp_employer, locals()), 2)
            formula_qp_employer = abs(formula_qp_employer) * legal.type_of_item

            pay_item: ItemPaid = ItemPaid.objects.create(**{
                'code': legal.code, 
                'name': legal.name,
                'type_of_item': legal.type_of_item, 
        
                'amount_qp_employer': formula_qp_employer, 
                'amount_qp_employee': formula_qp_employee, 

                'payslip': payslip})
            pay_items.append(pay_item)

        # Calculate the fixed value
        payslip.net = round(payslip.itempaid_set.all().aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.gross = round(payslip.itempaid_set.all().aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)

        payslip.taxable_gross = round(payslip.itempaid_set.all().aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.social_security_threshold = round(payslip.itempaid_set.all().aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        
        payslip.save()
        return payslip

    def tax(self, payslip, **kwargs):
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
        person = person if person > 0 else payslip.employee.child_set.count()
        person = person + (1 if payslip.employee.marital_status == 'Maried' else 0)

        ipr = ipr - ((ipr*0.02) * person)
        return round(ipr, 2)

app.register_task(Payer())
