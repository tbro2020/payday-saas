from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models import Base, fields
from django.db import models

from core.utils import upload_directory_file
from employee.models import Employee

class FundRequest(Base):
    employee = fields.ModelSelectField(Employee, verbose_name=_('employé'), on_delete=models.CASCADE)
    reason = fields.TextField(verbose_name=_('raison'), null=True, default=None)
    
    attach = fields.FileField(verbose_name=_('joindre'), blank=True, null=True, default=None, upload_to=upload_directory_file)
    devise = fields.CharField(verbose_name=_('devise'), max_length=20, default='CDF')
    amount = fields.FloatField(verbose_name=_('montant'), default=0.0)

    class Meta:
        verbose_name = _('demande de fond')
        verbose_name_plural = _('demande de fond')

    search_fields = ('employee__matricule', ' employee__last_name', 'employee__first_name', 'reason')
    list_display = ('id', 'employee', 'amount', 'devise', 'approved', 'updated_on')

    layout = Layout('employee', Row(Column('amount'), Column('devise')), 'attach', 'reason')
    _layout = Layout('employee', Row(Column('amount'), Column('devise')), 'attach', 'reason')

    @property
    def name(self):
        return f"Demande de fonds de {self.employee} #{self.id}"