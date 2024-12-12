from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import AceField
from core.models import Base


class TypeOfItems(models.IntegerChoices):
    Remunerative = (1, _('Remunerative'))
    Deductible = (-1, _('Deductible'))

class LegalItem(Base):
    code = models.CharField(_('code'), max_length=100, unique=True)
    type_of_item = models.IntegerField(_('type d\'element'), choices=TypeOfItems, default=TypeOfItems.Deductible)

    name = models.CharField(_('nom'), max_length=100)
    
    formula_qp_employer = AceField(mode='python', verbose_name=_('formule/montant quote part employeur'), default='0')
    formula_qp_employee = AceField(mode='python', verbose_name=_('formule/montant quote part employee'), default='0')

    condition = AceField(mode='python', verbose_name=_('condition'), default='0')

    list_display = ('code', 'type_of_item', 'name')
    list_filter = ('type_of_item',)
    
    layout = Layout(
        Row(Column('code', css_class='col-md-6 col-sm-12'), Column('type_of_item', css_class='col-md-6 col-sm-12')),
        'name',
        Column('condition', css_class='col-md-12 col-sm-12'),
        Row(
            Column('formula_qp_employer', css_class='col-md-12 col-sm-12'),
            Column('formula_qp_employee', css_class='col-md-12 col-sm-12')
        ),
        '_metadata'
    )

    class Meta:
        verbose_name = _('Retenue légale')
        verbose_name_plural = _('Retenues légales')
