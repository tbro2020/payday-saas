from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from django.db import models

from core.models.fields import ModelSelectField
from core.models import Base


class ItemPaid(Base):
    TYPE_OF_ITEMS = ((1, _('remunerative')), (-1, _('deductible')))
    
    type_of_item = models.IntegerField(_('type d\'element'), choices=TYPE_OF_ITEMS, default=1)
    code = models.CharField(_('code'), max_length=100)

    name = models.CharField(_('nom'), max_length=100)
    time = models.FloatField(_('temps'), default=0)
    rate = models.FloatField(_('taux'), default=0)
    
    amount_qp_employer = models.FloatField(verbose_name=_('montant quote part employeur'), default=0)
    amount_qp_employee = models.FloatField(verbose_name=_('montant quote part employee'), default=0)

    payslip = ModelSelectField('payroll.payslip', verbose_name=_('fiche de paie'), null=True, on_delete=models.CASCADE, editable=False)
    social_security_amount = models.FloatField(_('plafond de la sécurité sociale'), default=0)
    taxable_amount = models.FloatField(_('montant imposable'), default=0)

    is_bonus = models.BooleanField(_('est une prime'), help_text=_('Cet élément est un bonus'), default=False)
    is_payable = models.BooleanField(_('est payable'), help_text=_('Cet élément est payable'), default=True)

    list_display = ('payslip', 'code', 'name', 'amount_qp_employee', 'amount_qp_employer')
    list_filter = ('payslip__employee__registration_number', 'is_bonus', 'is_payable', 'type_of_item')

    def __str__(self):
        return f"Element payé {self.name} de la fiche de paie du {self.payslip.payroll.name}"
    
    list_filter = (
        "is_bonus",
        "is_payable",
    )

    layout = Layout(
        'name',
        'code',
        'time',
        'rate',
        'amount_qp_employer',
        'amount_qp_employee',
        'social_security_amount',
        'taxable_amount',
        'is_bonus',
        'is_payable'
    )

    class Meta:
        verbose_name = _('element payé')
        verbose_name_plural = _('elements payé')
