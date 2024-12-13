from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Row, Column

from core.models import fields
from core.models import Base
from django.db import models

class SpecialEmployeeItem(Base):
    employee = fields.ModelSelectField('employee.Employee', verbose_name=_('employee'), null = True, on_delete = models.SET_NULL)
    item = fields.ModelSelectField('payroll.Item', verbose_name=_('element de paie'), null = True, on_delete = models.SET_NULL, inline=True)
    amount_qp_employee = fields.FloatField(_('montant qp employé'), help_text=_('laisser vide pour utiliser la formule de l\'element'), default=None, null=True, blank=True, inline=True)
    amount_qp_employer = fields.FloatField(_('montant qp employeur'), help_text=_('laisser vide pour utiliser la formule de l\'element'), default=None, null=True, blank=True, inline=True)
    end_date = fields.DateField(_('date de fin'), inline=True, null=True, blank=True, default=None, help_text=_('laisser vide pour une date illimitée'))

    search_fields = ('employee__registration_number', 
                     'employee__middle_name', 
                     'employee__first_name', 
                     'employee__last_name', 
                    'item__code', 'item__name')
    
    list_filter = ('item', 'employee__status', 'created_at')
    list_display = ('id', 'employee', 'item')

    layout = Layout(
        'employee', 'item',
        Row(
            Column('amount_qp_employee', css_class='col-md-6 col-sm-12'),
            Column('amount_qp_employer', css_class='col-md-6 col-sm-12')
        ),
        'end_date'
    )
    

    @property
    def name(self):
        return self.employee.name + '/' + self.item.name

    class Meta:
        verbose_name = _('element special pour l\'employé')
        verbose_name_plural = _('element special pour l\'employé')