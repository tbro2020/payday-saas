from core.models.fields import ModelSelect, DateField, ModelSelect2Multiple
from crispy_forms.layout import Layout, Row, Column, Fieldset

from django.utils.translation import gettext as _

from core.models import Base
from django.db import models

class Claim(Base):
    employee = ModelSelect('employee.Employee', verbose_name=_('employé'), on_delete=models.CASCADE)
    payrolls = ModelSelect2Multiple('payroll.payroll', verbose_name=_('paies'))
    period = DateField(verbose_name=_('periode de la paie'))

    description = models.TextField(verbose_name=_("description"), help_text=_("Décrivez en quelques mots la demande"))
    solved = models.BooleanField(verbose_name=_("Est résolu ?"), help_text=_("coche si le problème a été résolu"))

    list_display = ['employee', 'period', 'solved']
    list_filter = ['period', 'solved']

    layout = Layout(
        'employee',
        'payrolls',
        'period',
        Fieldset(
            _('Informations sur le probleme'),
            Row(
                Column('description', css_class='form-group col-md-12'),
                Column('solved', css_class='form-group col-md-12'),
            )
        )
    )

    @property
    def name(self):
        return f'Réclamation du {self.period} de {self.employee.registration_number}'

    class Meta:
        verbose_name = _('Réclamation')
        verbose_name_plural = _('Réclamations')