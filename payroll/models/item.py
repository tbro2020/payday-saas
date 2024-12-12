from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import AceField
from core.models import Base


class Item(Base):
    TYPE_OF_ITEMS = ((1, _('Remunerative')), (-1, _('Deductible')))

    type_of_item = models.IntegerField(_('type d\'element'), choices=TYPE_OF_ITEMS, default=1)
    code = models.CharField(_('code'), max_length=100, unique=True)
    name = models.CharField(_('nom'), max_length=100)

    formula_qp_employer = AceField(mode='python', verbose_name=_('formule/montant quote part employeur'), default='0')
    formula_qp_employee = AceField(mode='python', verbose_name=_('formule/montant quote part employee'), default='0')

    condition = AceField(mode='python', verbose_name=_('condition'), default='0')
    time = AceField(mode='python', verbose_name=_('temps'), default='0')

    is_social_security = models.BooleanField(_('est éligible à la sécurité sociale'), help_text=_('Cet élément fera partie du seuil de sécurité sociale'), default=False)
    is_taxable = models.BooleanField(_('est impossable'), help_text=_('Cet élément fera partie du montant brut imposable'), default=False)
    
    is_bonus = models.BooleanField(_('est une prime'), help_text=_('Cet élément est un bonus'), default=False)
    is_payable = models.BooleanField(_('est payable'), help_text=_('Cet élément est payable'), default=True)
    

    list_display = ('code', 'name', 'is_taxable', 'is_social_security')
    list_filter = ('type_of_item', 'is_taxable', 'is_social_security')
    
    layout = Layout(
        Row(Column('code', css_class='col-md-6 col-sm-12'), Column('type_of_item', css_class='col-md-6 col-sm-12')),
        'name',
        Column('condition', css_class='col-md-12 col-sm-12'),
        Column('time', css_class='col-md-12 col-sm-12'),
        Row(
            Column('formula_qp_employee', css_class='col-md-12 col-sm-12'),
            Column('formula_qp_employer', css_class='col-md-12 col-sm-12')
        ),
        Row(
            Column('is_bonus', css_class='col-md-6 col-sm-12'),
            Column('is_payable', css_class='col-md-6 col-sm-12'),
            Column('is_taxable', css_class='col-md-6 col-sm-12'),
            Column('is_social_security', css_class='col-md-6 col-sm-12')
        ),
        '_metadata'
    )

    class Meta:
        verbose_name = _('element de paie')
        verbose_name_plural = _('elements de paie')
        
    def __str__(self):
        return self.name
