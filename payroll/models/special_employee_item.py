from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from django.db import models

from core.models.fields import ModelSelect
from core.models import Base

class SpecialEmployeeItem(Base):
    amount_qp_employee = models.FloatField(_('montant qp employé'), help_text=_('laisser vide pour utiliser la formule de l\'element'), default=None, null=True, blank=True)
    employee = ModelSelect('employee.Employee', verbose_name=_('employee'), null = True, on_delete = models.SET_NULL)
    item = ModelSelect('payroll.Item', verbose_name=_('element de paie'), null = True, on_delete = models.SET_NULL)

    inline_form_fields = ('employee', 'item', 'amount_qp_employee')
    list_display = ('id', 'employee', 'item')

    @property
    def name(self):
        return self.employee.name
    
    layout = Layout('employee', 'item')

    class Meta:
        verbose_name = _('element special pour l\'employé')
        verbose_name_plural = _('element special pour l\'employé')