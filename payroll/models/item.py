from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import AceField
from core.models import Base


class Item(Base):
    TYPE_OF_ITEMS = ((1, _('Remunerative')), (-1, _('Deductible')))

    code = models.CharField(_('code'), max_length=100, unique=True)
    type_of_item = models.IntegerField(_('type d\'element'), choices=TYPE_OF_ITEMS, default=1)

    name = models.CharField(_('nom'), max_length=100)
    time = AceField(mode='python', verbose_name=_('temps'), default='0')

    formula = AceField(mode='python', verbose_name=_('forumule/montant'), default='0')
    condition = AceField(mode='python', verbose_name=_('condition'), default='0')

    is_payable = models.BooleanField(_('est payable'), help_text=_('Cet élément est payable'), default=True)
    is_taxable = models.BooleanField(_('is impossable'), help_text=_('Cet élément fera partie du montant brut imposable'), default=False)
    is_social_security = models.BooleanField(_('est éligible à la sécurité sociale'), help_text=_('Cet élément fera partie du seuil de sécurité sociale'), default=False)

    list_display = ('code', 'type_of_item', 'name', 'is_taxable', 'is_social_security')
    list_filter = ('type_of_item', 'is_taxable', 'is_social_security')
    layout = Layout(
        Row(Column('code'), Column('type_of_item')),
        'name', 'condition',
        Row(Column('time', css_class='col-4'), Column('formula', css_class='col-8')),
        Row(Column('is_payable'), Column('is_taxable'), Column('is_social_security')),
        'metadata'
    )

    class Meta:
        verbose_name = _('element de paie')
        verbose_name_plural = _('elements de paie')
        
    def __str__(self):
        return self.name
