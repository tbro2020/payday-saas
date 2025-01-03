from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db import models

from core.models.fields import ModelSelectField
from core.models import Base


class Payslip(Base):
    employee = ModelSelectField('payroll.paidemployee', verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    payroll = ModelSelectField('payroll.payroll', verbose_name=_('paie'), null=True, on_delete=models.CASCADE)

    social_security_threshold = models.FloatField(_('plafond cnss/cnsap'), default=0)
    taxable_gross = models.FloatField(_('brut imposable'), default=0)
    
    gross = models.FloatField(_('brut'), default=0)
    net = models.FloatField(_('net'), default=0)

    search_fields = ['employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name']
    list_filter = ('employee__branch', 'employee__direction', 'employee__sub_direction', 'employee__status')
    list_display = ('id', 'employee', 'payroll', 'gross', 'taxable_gross', 'net')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('fiche de paie')
        verbose_name_plural = _('fiches de paie')

    @property
    def get_action_buttons(self):
        return [{
            'text': _('Imprimer'),
            'url': reverse_lazy('payroll:slips')+'?pk='+str(self.pk),
            'classes': 'btn btn-light-info',
            'tag': 'a',
        }]

    @property
    def name(self):
        return f"Fiche de paie de {self.employee.name} de la paie {self.payroll.name}"
    
    def __str__(self):
        return f"Fiche de paie de {self.employee.name} de la paie {self.payroll.name}"
    
    def get_absolute_url(self):
        return reverse_lazy('payroll:payslip', kwargs={'pk': self.pk})
    
    def is_not_payable_items(self):
        return self.itempaid_set.filter(is_payable=False)

    class Meta:
        verbose_name = _('fiche de paie')
        verbose_name_plural = _('fiches de paie')

    def refresh(self):
        items_paid = self.itempaid_set.filter(is_payable=True)
        
        social_security_amount = round(items_paid.aggregate(amount=models.Sum('social_security_amount'))['amount'] or 0, 2)
        amount_qp_employee = round(items_paid.aggregate(amount=models.Sum('amount_qp_employee'))['amount'] or 0, 2)
        taxable_amount = round(items_paid.aggregate(amount=models.Sum('taxable_amount'))['amount'] or 0, 2)

        self.social_security_threshold = social_security_amount
        self.taxable_gross = taxable_amount
        self.gross = amount_qp_employee
        self.net = amount_qp_employee
        self.save()

    def refresh_legals_items(self):
        from django.apps import apps
        legal_items = apps.get_model('payroll', 'legalitem').objects.all()
        self.itempaid_set.filter(legal_item__in=legal_items).delete()
        items_paid = self.itempaid_set.all()
        
        for legal in legal_items:
            _locals = {'employee': self.employee, 'payroll': self.payroll, 'payslip': self, 'item': legal, 'items_paid': items_paid}

            amount_qp_employee = eval(legal.amount_qp_employee, locals=_locals) or 0
            amount_qp_employer = eval(legal.amount_qp_employee, locals=_locals) or 0

            amount_qp_employee = round(abs(amount_qp_employee), 2) * legal.type_of_item
            amount_qp_employer = round(abs(amount_qp_employer), 2) * legal.type_of_item

            item = legal.itempaid_set.create(**{
                'code': legal.code,
                'type_of_item': legal.type_of_item,
                'name': legal.name, 'time': 0, 'rate': 0,
                'amount_qp_employee': amount_qp_employee,
                'amount_qp_employer': amount_qp_employer,
                'social_security_amount': 0,
                'taxable_amount': 0,
                'is_payable': True,
                'is_bonus': False,
                'payslip': self
            })
            item.save()

        return self.itempaid_set.all()


    def approved(self):
        return self.payroll.approved()
