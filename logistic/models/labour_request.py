from crispy_forms.layout import Layout
from core.models import Base, fields
from employee.models import Employee

from django.utils.translation import gettext as _
from django.db import models

class LabourRequest(Base):
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    description = fields.TextField(verbose_name=_('description'), blank=True)

    class Meta:
        verbose_name = _('demande de main-d\'œuvre')
        verbose_name_plural = _('demande de main-d\'œuvre')

    search_fields = ('employee__matricule', ' employee__last_name', 'employee__first_name', 'description')
    list_display = ('id', 'employee', 'approved', 'updated_on')
    inlines = ('logistic.Labour',)

    layout = Layout('employee', 'description')
    _layout = Layout('employee', 'description')

    @property
    def name(self):
        return f"{self.employee} / {self.description}"


class Labour(Base):
    labourrequest = fields.ForeignKey(LabourRequest, verbose_name=_('demande de main-d\'œuvre #'), on_delete=models.CASCADE)
    designation = fields.CharField(verbose_name=_('désignation'), max_length=250, null=True, default=None, inline=True, approver=True)
    destination = fields.CharField(verbose_name=_('destination'), max_length=250, null=True, default=None, inline=True, approver=True)
    observation =fields.CharField(verbose_name=_('observation'), max_length=250, null=True, default=None, inline=True, approver=True)
    provenance = fields.CharField(verbose_name=_('provenance'), max_length=250, null=True, default=None, inline=True, approver=True)
    quantity = fields.FloatField(verbose_name=_('quantité'), default=0.0, approver=True)

    class Meta:
        verbose_name = _('labour')
        verbose_name_plural = _('labours')

    @property
    def name(self):
        return f"{self.labourrequest} / {self.designation}"