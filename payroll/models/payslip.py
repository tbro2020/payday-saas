from api.serializers import model_serializer_factory
from django.utils.translation import gettext as _

from django.urls import reverse_lazy
from django.db import models

from employee.models import Employee
from payroll.models import Payroll

from core.models.fields import ModelSelect
from core.models import Base


EmployeeSerializer = model_serializer_factory(Employee)

class Payslip(Base):
    payroll = models.ForeignKey(Payroll, verbose_name=_('paie'), null=True, on_delete=models.CASCADE)

    social_security_threshold = models.FloatField(_('plafond cnss/cnsap'), default=0)
    taxable_gross = models.FloatField(_('brut imposable'), default=0)
    
    gross = models.FloatField(_('brut'), default=0)
    net = models.FloatField(_('net'), default=0)

    employee = ModelSelect('payroll.employee', verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    
    search_fields = ['employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name']
    list_display = ('id', 'employee', 'gross', 'taxable_gross', 'net')

    @property
    def name(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('payroll:payslip', kwargs={'pk': self.pk})
    
    def is_not_payable_items(self):
        return self.itempaid_set.filter(is_payable=False)

    class Meta:
        verbose_name = _('fiche de paie')
        verbose_name_plural = _('fiches de paie')

    def approved(self):
        return self.payroll.approved()
