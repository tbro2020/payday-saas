from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db import models

from .payroll import Payroll
from core.models import Base


class Payslip(Base):
    social_security_threshold = models.FloatField(_('plafond cnss/cnsap'), default=0)
    taxable_gross = models.FloatField(_('brut imposable'), default=0)
    
    gross = models.FloatField(_('brut'), default=0)
    net = models.FloatField(_('net'), default=0)

    employee = models.ForeignKey('employee.Employee', verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    payroll = models.ForeignKey(Payroll, verbose_name=_('paie'), null=True, on_delete=models.CASCADE)

    # employee current situation a kind of static copy of the object

    list_filter = ('employee__registration_number', 'employee__branch', 'employee__grade', 
                   'employee__payer_name', 'employee__status', 'employee__date_of_birth', 'employee__date_of_join')
    search_fields = ['employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name']
    list_display = ('id', 'employee', 'gross', 'taxable_gross', 'net')

    @property
    def name(self):
        return self.employee.name

    def get_absolute_url(self):
        return reverse_lazy('payroll:payslip', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('fiche de paie')
        verbose_name_plural = _('fiches de paie')

    def approved(self):
        return self.payroll.approved()
