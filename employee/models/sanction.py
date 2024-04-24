from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from core.models import Base

from django.db import models

class SanctionType(Base):
    name = models.CharField(verbose_name=_('nom'),max_length=255)

class Sanction(Base):
    sanction_type = ModelSelect('employee.sanctiontype', on_delete=models.SET_NULL, null=True)
    employee = ModelSelect('employee.employee', on_delete=models.SET_NULL, null=True)

    _from_date = models.DateField(verbose_name=_('date de début'))
    _to_date = models.DateField(verbose_name=_('date de fin'))

    description = models.TextField(verbose_name=_('description'), null=True)
    reason = models.TextField(verbose_name=_('motif'), null=True)

    @property
    def name(self):
        return "Sanction de %s" % self.employee
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('sanction')
        verbose_name_plural = _('sanctions')
    