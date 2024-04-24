from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import ModelSelect, TimeField, DateField
from django.forms import ValidationError
from core.models import Base, Preference

from employee.models import Employee
from datetime import datetime

class EarlyLeave(Base):
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, default=None, on_delete=models.SET_NULL)
    destination = models.CharField(verbose_name=_('destination'), max_length=250, null=True, default=None)
    date = DateField(verbose_name=_('date'), default=datetime.today)

    start_time = TimeField(verbose_name=_('de'))
    end_time = TimeField(verbose_name=_('à'))
    
    observation = models.TextField(verbose_name=_('observation'), blank=True, null=True, default=None)
    reason = models.TextField(verbose_name=_('motif'))

    list_filter = ('start_time', 'end_time', 'date')
    list_display = ('id', 'employee', 'start_time', 'end_time')
    layout = Layout('employee', 'destination', Row(Column('start_time'), Column('end_time')), 'reason', 'observation')
    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name') 

    @property
    def name(self):
        return '{employee} de {start} à {end}'.format(**{
            'employee': self.employee.full_name(),
            'start': self.start_time,
            'end': self.end_time
        })
    
    def clean(self):
        preference = Preference.get('EARLY_LEAVE_START_TIME_HOUR')
        if not preference: return super().clean()
        if int(preference.value) > int(self.start_time.split(':')[0]):
            raise ValidationError(_('Vous ne pouvez pas faire de demande avant %s heures du matin') % (preference.value))
        return super().clean()
    
    class Meta:
        verbose_name = _('bon de sortie anticipé')
        verbose_name_plural = _('bon de sortie anticipé')
