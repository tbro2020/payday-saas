from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from employee.models import Employee
from django.db.models import Sum
from payroll.models import *
from celery import Task

from employee.models import MaritalStatus
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
            'grade__in': self.payroll.employee_grade.values_list('id'),
            'branch__in': self.payroll.employee_branch.values_list('id'),
            'status__in': self.payroll.employee_status.values_list('id'),
            'direction__in': self.payroll.employee_direction.values_list('id')
        }
        payroll_employee_filter = {k:v for k,v in payroll_employee_filter.items() if v}
        self.employees = self.employees.filter(**payroll_employee_filter).filter(**kwargs.get('employee', {}))
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
        items_to_pay = []
        payslip, created = Payslip.objects.get_or_create(
            employee=employee, 
            payroll=self.payroll, 
            created_by=self.payroll.created_by
        )
        items_paid_code = payslip.itempaid_set.values_list('code', flat=True)

        for item in self.items:
            if item.code in items_paid_code: continue
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
            item_to_pay: ItemPaid = ItemPaid(**{'code': item.code, 
                'type_of_item': item.type_of_item, 

                'name': item.name, 
                'time': time, 
                'rate': rate,

                'amount_qp_employer': formula_qp_employer, 
                'amount_qp_employee': formula_qp_employee, 

                'taxable_amount': formula_qp_employee if item.is_taxable else 0,
                'social_security_amount': formula_qp_employee if item.is_social_security else 0,

                'is_bonus': item.is_bonus,
                'is_payable': item.is_payable,
                
                'payslip': payslip,
                'created_by': self.payroll.created_by
            })
            items_to_pay.append(item_to_pay)
        ItemPaid.objects.bulk_create(items_to_pay)

        # Calculate the fixed value
        items_paid = payslip.itempaid_set.filter(is_payable=True)
        payslip.gross = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.net = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)

        payslip.social_security_threshold = round(items_paid.aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        payslip.taxable_gross = round(items_paid.aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.save()

        return payslip

    def _duty(self, payslip: Payslip):
        legal_items_to_pay = []
        qs = payslip.itempaid_set.filter(code__in=[item.code for item in self.legal_items])
        qs.order_by().select_related(None)._raw_delete(qs.db)

        for legal in self.legal_items:
            condition = eval(legal.condition, locals())
            if not condition: continue

            # formula qp employee
            formula_qp_employee = round(eval(legal.formula_qp_employee, locals()), 2)
            formula_qp_employee = abs(formula_qp_employee) * legal.type_of_item

            # formula qp employer
            formula_qp_employer = round(eval(legal.formula_qp_employer, locals()), 2)
            formula_qp_employer = abs(formula_qp_employer) * legal.type_of_item

            legal_item_to_pay: ItemPaid = ItemPaid(**{
                'code': legal.code, 
                'name': legal.name,
                'type_of_item': legal.type_of_item, 
        
                'amount_qp_employer': formula_qp_employer, 
                'amount_qp_employee': formula_qp_employee, 

                'is_bonus': False,
                'is_payable': True,

                'payslip': payslip,
                'created_by': self.payroll.created_by
            })
            legal_items_to_pay.append(legal_item_to_pay)

        # Calculate the fixed value
        ItemPaid.objects.bulk_create(legal_items_to_pay)
        items_paid = payslip.itempaid_set.filter(is_payable=True)
        payslip.net = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
        payslip.gross = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)

        payslip.taxable_gross = round(items_paid.aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
        payslip.social_security_threshold = round(items_paid.aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
        
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
        person = person + (1 if payslip.employee.marital_status == MaritalStatus.Maried.value else 0)

        ipr = ipr - ((ipr*0.02) * person)
        return round(ipr, 2)

app.register_task(Payer())
