from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Row, Column
from django.db import models

from core.models.fields import ModelSelect
from core.models import Base

class SpecialEmployeeItem(Base):
    amount_qp_employer = models.FloatField(_('montant qp employeur'), help_text=_('laisser vide pour utiliser la formule de l\'element'), default=None, null=True, blank=True)
    amount_qp_employee = models.FloatField(_('montant qp employé'), help_text=_('laisser vide pour utiliser la formule de l\'element'), default=None, null=True, blank=True)
    
    employee = ModelSelect('employee.Employee', verbose_name=_('employee'), null = True, on_delete = models.SET_NULL)
    item = ModelSelect('payroll.Item', verbose_name=_('element de paie'), null = True, on_delete = models.SET_NULL)

    search_fields = ('employee__registration_number', 'employee__middle_name', 'employee__first_name', 'employee__last_name', 
                    'item__code', 'item__name')
    inline_form_fields = ('employee', 'item', 'amount_qp_employee', 'amount_qp_employer')
    
    list_filter = ('item', 'employee__status')
    list_display = ('id', 'employee', 'item')

    layout = Layout(
        'employee', 'item',
        Row(
            Column('amount_qp_employee', css_class='col-md-6 col-sm-12'),
            Column('amount_qp_employer', css_class='col-md-6 col-sm-12')
        ),
    )
    

    @property
    def name(self):
        return self.employee.name + '/' + self.item.name

    class Meta:
        verbose_name = _('element special pour l\'employé')
        verbose_name_plural = _('element special pour l\'employé')