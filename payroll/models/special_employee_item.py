from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from django.db import models

from core.models.fields import ModelSelect
from core.models import Base

class SpecialEmployeeItem(Base):
    employee = ModelSelect('employee.Employee', verbose_name=_('employee'), null = True, on_delete = models.SET_NULL)
    item = ModelSelect('payroll.Item', verbose_name=_('element de paie'), null = True, on_delete = models.SET_NULL)
    condition = models.CharField(_('condition'), max_length=255, default='1')

    inline_form_fields = ('employee', 'item', 'condition')
    list_display = ('id', 'employee', 'item')

    @property
    def name(self):
        return self.employee.name
    
    layout = Layout('employee', 'item')

    class Meta:
        verbose_name = _('element special pour l\'employé')
        verbose_name_plural = _('element special pour l\'employé')