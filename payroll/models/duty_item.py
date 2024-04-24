from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import AceField
from core.models import Base


class DutyItem(Base):
    TYPE_OF_ITEMS = ((1, _('Remunerative')), (-1, _('Deductible')))

    code = models.CharField(_('code'), max_length=100, unique=True)
    type_of_item = models.IntegerField(_('type d\'element'), choices=TYPE_OF_ITEMS, default=1)

    name = models.CharField(_('nom'), max_length=100)

    time = AceField(mode='python', verbose_name=_('temps'), default='0')
    condition = AceField(mode='python', verbose_name=_('condition'), default='0')
    formula = AceField(mode='python', verbose_name=_('formule/montant'), default='0')

    list_display = ('code', 'type_of_item', 'name')
    list_filter = ('type_of_item',)
    
    layout = Layout(
        Row(Column('code'), Column('type_of_item')),
        'name', 'condition',
        Row(Column('time'), Column('formula')),
        'metadata'
    )

    class Meta:
        verbose_name = _('autre element')
        verbose_name_plural = _('autre elements')
