from core.models.fields import ModelSelectField, DateField, FloatField
from crispy_forms.layout import Layout, Row, Column, Fieldset
from django.utils.translation import gettext as _

from core.models import Base
from django.db import models

class AdvanceSalary(Base):
    employee = ModelSelectField('employee.employee', verbose_name=_('employé'), on_delete=models.CASCADE)
    duration = models.IntegerField(_('durée'), help_text=_('nombre de mois'), default=36)
    amount = models.FloatField(_('montant'))
    date = DateField(_('date'))

    list_display = ['employee', 'amount', 'date', 'duration']
    inlines = ['payroll.advancesalarypayment']

    layout = Layout(
        'employee',
        'date',
        Fieldset(
            _('Informations sur l\'avance de salaire'),
            Row(
                Column('amount', css_class='form-group col-md-12'),
                # Column('duration', css_class='form-group col-md-6'),
            )
        )
    )

    @property
    def name(self):
        return f'Avance de salaire de {self.employee} du {self.date}'

    class Meta:
        verbose_name = _('avance sur salaire')
        verbose_name_plural = _('avances sur salaire')

class AdvanceSalaryPayment(Base):
    advance_salary = ModelSelectField('payroll.AdvanceSalary', verbose_name=_('avance de salaire'), on_delete=models.CASCADE)
    amount = FloatField(_('montant'), inline=True)
    date = DateField(_('date'), inline=True)

    list_display = ['advance_salary', 'amount', 'date']
    list_filter = ['date']

    layout = Layout(
        'advance_salary',
        'amount',
        'date'
    )

    @property
    def name(self):
        return f'Paiement d\'avance de salaire de {self.advance_salary.employee} du {self.date}'

    class Meta:
        verbose_name = _('paiement d\'avance de salaire')
        verbose_name_plural = _('paiements d\'avance de salaire')