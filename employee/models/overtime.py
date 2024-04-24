from core.models.fields import ModelSelect, DateField, TimeField
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models import Base
from django.db import models

from .employee import Employee


class Overtime(Base):
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, on_delete=models.SET_NULL)
    reason = models.TextField(_('motif'), null=True, default=None)

    from_time = TimeField(verbose_name=_('de'))
    to_time = TimeField(verbose_name=_('à'))
    date = DateField(verbose_name=_('date'))

    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name') 
    layout = Layout('approvers', 'employee', Row(Column('date'), Column('from_time'), Column('to_time')), 'reason')
    _layout = Layout('employee', Row(Column('date'), Column('from_time'), Column('to_time')), 'reason')
    list_display = ('id', 'employee', 'date', 'from_time', 'to_time')
    inline_form_fields = ('date', 'from_time', 'to_time')

    @property
    def name(self):
        return f"Heures supplémentaires #{self.id} de {self.employee}"

    class Meta:
        verbose_name = _('Heure supplémentaires')
        verbose_name_plural = _('Heures supplémentaires')
