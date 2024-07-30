from core.models.fields import ModelSelect, DateField
from django.utils.translation import gettext as _
from core.models import Base
from django.db import models


class Commission(Base):
    employee = ModelSelect('employee.employee', verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    grade = ModelSelect('employee.grade', verbose_name=_('grade'), null=True, on_delete=models.SET_NULL)
    
    start_dt = DateField(verbose_name='date de début')
    end_dt = DateField(verbose_name='date de fin')

    @property
    def name(self):
        return self.employee

    def __str__(self):
        return f"{self.employee} - {self.grade_interim}"
    
    class Meta:
        verbose_name = _('commission')
        verbose_name_plural = _('commissions')