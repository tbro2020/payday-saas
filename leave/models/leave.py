from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.utils import upload_directory_file
from core.models import Base, fields

from .type_of_leave import TypeOfLeave
from employee.models import Employee
from django import forms


class Leave(Base):
    type_of_leave = fields.ModelSelectField(TypeOfLeave, verbose_name=_('type de congé'), on_delete=models.CASCADE)
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    
    days = fields.IntegerField(verbose_name=_('jours'), editable=False, default=0)
    return_dt = fields.DateField(verbose_name=_('date de retour'))
    start_dt = fields.DateField(verbose_name=_('du'))
    end_dt = fields.DateField(verbose_name=_('au'))
    
    attach = models.FileField(verbose_name=_('joindre'), blank=True, null=True, default=None, upload_to=upload_directory_file)
    reason = models.TextField(verbose_name=_('motif'), null=True, default=None)

    list_filter = ('start_dt', 'end_dt')
    list_display = ('id', 'employee', 'start_dt', 'end_dt', 'approved', 'reason')
    _layout = Layout(Row(Column('type_of_leave'), Column('employee')), Row(Column('start_dt'), Column('end_dt'), Column('return_dt')), 'reason', 'attach')
    layout = Layout(Row(Column('type_of_leave'), Column('employee')), Row(Column('start_dt'), Column('end_dt'), Column('return_dt')), 'reason', 'attach')
    search_fields = ('employee__registration_number', 'employee__first_name', 'employee__middle_name', 'employee__last_name') 

    @property
    def name(self):
        return f"{self.employee} for {self.type_of_leave}"
    
    def clean(self):
        taken_days = Leave.objects.filter(employee=self.employee, type_of_leave=self.type_of_leave)
        taken_days = sum([leave.days for leave in taken_days])

        if taken_days + self.days > self.type_of_leave.max_days_per_year:
            raise forms.ValidationError(_("Jours demandés({}) + Jours pris ({}) > Total des jours restants ({}) du {}").format(self.days, taken_days, self.type_of_leave.max_days_per_year, self.type_of_leave.name))
    
    # before save fill the field days with the number of days between start_dt and end_dt
    def save(self, *args, **kwargs):
        self.days = (self.end_dt - self.start_dt).days
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('congé')
        verbose_name_plural = _('congés')