from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from employee.models import Employee
from django.db.models import Sum
from payroll.models import *
from celery import Task

from payday.celery import app

class Payer(Task):
    errors = []
    ignore_result = True
    name = 'payday.payroll.payer.Payer'

    items = Item.objects.all()
    duty_items = DutyItem.objects.all()
    employees = Employee.objects.select_related().all()

    def run(self, payroll, *args, **kwargs):
        if not isinstance(payroll, Payroll):
            payroll = get_object_or_404(Payroll, pk=payroll)
        self.payroll = payroll

        # fetch employees
        employees = self.payroll.metadata.get('employee', {})
        self.employees = self.employees.filter(**employees)
        self.employees = self.employees.filter(**kwargs.get('employee', {}))
        
        payroll_employee_filter = {
            'grade__in': self.payroll.grade.all(),
            'branch__in': self.payroll.branch.all(),
            'direction__in': self.payroll.direction.all(),
            #'payer_name__in': self.payroll.payer_name.all(),
            #'status__in': self.payroll.employee_status.all()
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
            self.payroll.status = 'SUCCESS'
            self.payroll.save()
        except Exception as ex:
            self.payroll.status = 'WARNING'
            self.payroll.metadata['errors'].append({'message': str(ex), 'tag': 'error'})
            self.payroll.created_by.email_user(_(f"Il semble que quelque chose n'a pas fonctionné dans votre système de paie {self.payroll.name}"), str(ex))
            self.payroll.save()

    def _payslip(self, employee: Employee):
        pay_items = []
        payslip, created = Payslip.objects.get_or_create(employee=employee, payroll=self.payroll)

        for item in self.items:
            condition = eval(item.condition, locals())
            if not condition: continue

            time = eval(item.time, locals())
            amount = round(eval(item.formula, locals()), 2)
            amount = abs(amount) * item.type_of_item
            if amount == 0: continue

            rate = (amount / time) if time > 0 else amount
            rate = round(abs(rate), 2)

            pay_item: PayItem = PayItem.objects.create(
                **{'code': item.code, 'type_of_item': item.type_of_item, 
                   'name': item.name, 'time': time, 'rate': rate,
                   'amount': amount, 'taxable_amount': amount if item.is_taxable else 0,
                   'social_security_amount': amount if item.is_social_security else 0, 'payslip': payslip})
            pay_items.append(pay_item)

        if not created:
            payslip.payitem_set.filter(code__in=[item.code for item in pay_items]).delete()

        # Calculate the fixed value
        payslip.net = round(payslip.payitem_set.all().aggregate(amount=Sum('amount')).get('amount', 0), 2)
        payslip.gross = round(payslip.payitem_set.all().aggregate(amount=Sum('amount')).get('amount', 0), 2)
        payslip.taxable_gross = round(payslip.payitem_set.all().aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.social_security_threshold = round(payslip.payitem_set.all().aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        payslip.save()

        return payslip

    def _duty(self, payslip: Payslip):
        pay_items = []

        for duty in self.duty_items:
            print(duty)
            condition = eval(duty.condition, locals())
            if not condition: continue

            time = eval(duty.time)

            amount = round(eval(duty.formula, locals()), 2)
            amount = abs(amount) * duty.type_of_item

            pay_item: PayItem = PayItem.objects.create(**{
                'code': duty.code, 'type_of_item': duty.type_of_item, 
                'name': duty.name, 'time': time, 'amount': amount, 'payslip': payslip})
            pay_items.append(pay_item)

        # Calculate the fixed value
        payslip.net = round(payslip.payitem_set.all().aggregate(amount=Sum('amount')).get('amount', 0), 2)
        payslip.gross = round(payslip.payitem_set.all().aggregate(amount=Sum('amount')).get('amount', 0), 2)
        payslip.taxable_gross = round(payslip.payitem_set.all().aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.social_security_threshold = round(payslip.payitem_set.all().aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        payslip.save()
        return payslip

    def _ipr(self, payslip, **kwargs):
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
