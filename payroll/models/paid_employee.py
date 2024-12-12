from django.utils.translation import gettext as _
from core.models.fields import ModelSelectField
from employee.models.base import Employee
from django.urls import reverse_lazy
from django.db import models

class PaidEmployee(Employee):
    photo = None
    payroll = ModelSelectField('payroll.payroll', verbose_name=_('paie'), blank=True, null=True, default=None, on_delete=models.SET_NULL)

    @property
    def name(self):
        return self.short_name()
    
    def get_absolute_url(self):
        return reverse_lazy("employee:change", kwargs={"pk": self.registration_number})

    class Meta:
        verbose_name = _('employé rémunéré')
        verbose_name_plural = _('employés rémunéré')
        ordering = ('-status', 'registration_number')