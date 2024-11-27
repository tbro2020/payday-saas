from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models import Base, fields
from employee.models import Employee
from datetime import datetime

class EarlyLeave(Base):
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)

    destination = fields.CharField(verbose_name=_('destination'), max_length=250, null=True, default=None)
    date = fields.DateField(verbose_name=_('date'), default=datetime.today)
    start_time = fields.TimeField(verbose_name=_('de'))
    end_time = fields.TimeField(verbose_name=_('à'))
    
    reason = fields.TextField(verbose_name=_('motif'))
    observation = fields.TextField(verbose_name=_('observation'), blank=True, null=True, default=None)

    list_filter = ('start_time', 'end_time', 'date')
    list_display = ('id', 'employee', 'start_time', 'end_time', 'approved')
    _layout = Layout('employee', 'destination', Row(Column('start_time'), Column('end_time')), 'reason', 'observation')
    layout = Layout('employee', 'destination', Row(Column('start_time'), Column('end_time')), 'reason', 'observation')
    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name') 

    @property
    def name(self):
        return '{employee} de {start} à {end}'.format(**{
            'employee': self.employee.full_name(),
            'start': self.start_time,
            'end': self.end_time
        })
    
    class Meta:
        verbose_name = _('départ anticipé')
        verbose_name_plural = _('départs anticipé')
