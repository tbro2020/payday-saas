from django.utils.translation import gettext as _
from django.db import models
from core.models import Base


class AdvanceSalary(Base):
    employee = models.ForeignKey('employee.Employee', verbose_name=_('employé'), on_delete=models.CASCADE)

    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("montant initial"))
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("mensualités"))
    start_dt = models.DateField(verbose_name=_("date de début"))
    end_dt = models.DateField(verbose_name=_("date de fin"))

    class Meta:
        verbose_name = _('Avance sur salaire')
        verbose_name_plural = _('Avances sur salaire')
        
    def __str__(self):
        return self.name
