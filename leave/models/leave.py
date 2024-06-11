from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.forms import ValidationError
from django.db import models

from core.models.fields import ModelSelect, DateField
from core.models import Base

from .type_of_leave import TypeOfLeave
from employee.models import Employee


class Leave(Base):
    interim = ModelSelect(Employee, verbose_name=_('remplaçant'), null=True, default=None, on_delete=models.SET_NULL, related_name='interim')
    type_of_leave = ModelSelect(TypeOfLeave, verbose_name=_('type de congé'), null=True, default=None, on_delete=models.SET_NULL)
    employee = ModelSelect(Employee, verbose_name=_('employé'), null=True, default=None, on_delete=models.SET_NULL)

    reason = models.TextField(verbose_name=_('motif'), null=True, default=None)
    start_dt = DateField(verbose_name=_('du'))
    end_dt = DateField(verbose_name=_('au'))

    layout = Layout('type_of_leave', Row(Column('employee', css_class='col-md-6 col-sm-12'), Column('interim', css_class='col-md-6 col-sm-12')), Row(Column('start_dt', css_class='col-md-6 col-sm-12'), Column('end_dt', css_class='col-md-6 col-sm-12')), 'reason')
    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name') 
    list_display = ('id', 'employee', 'interim', 'start_dt', 'end_dt')
    list_filter = ('start_dt', 'end_dt')
    change_list_template = 'leave/change_list.html'
    
    @property
    def name(self):
        return f"{self.type_of_leave} de {self.employee}"
    
    @property
    def days(self):
        return (self.end_dt - self.start_dt).days
    
    @property
    def taken(self):
        return sum([leave.days for leave in Leave.objects.filter(employee=self.employee)])

    @property
    def available_days(self):
        return self.type_of_leave.max_days_per_year - self.taken
    
    def clean(self):
        available_days = self.available_days
        if self.days > available_days:
            raise ValidationError(_('vous ne pouvez pas demander plus de jours que ceux disponibles (Il vous reste %d jour(s))') 
                                  % (available_days))
        return super().clean()

    class Meta:
        verbose_name = _('congé')
        verbose_name_plural = _('congés')

        #managed = False
        #db_table = 'leave'