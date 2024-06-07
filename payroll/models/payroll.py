from crispy_forms.bootstrap import FieldWithButtons, Field, StrictButton
from crispy_forms.layout import Layout, Row, Column

from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db import models

from core.models.fields import ModelSelect2Multiple
from core.models.fields import DateField, JSONField
from core.utils import upload_directory_file
from django.urls import reverse_lazy
from core.models import Base



leave_empty_for_all = _('laisser vide pour tous')

class PayrollStatus(models.TextChoices):
    WARNING = ('WARNING', _('avertissement'))
    PROGRESS = ('PROGRESS', _('en cours'))
    SUCCESS = ('SUCCESS', _('succès'))

class Payroll(Base):
    def _metadata():
        return dict(taux=2000, litrage=3650)

    additional_items = models.FileField(verbose_name=_('éléments additionnels'), upload_to=upload_directory_file, blank=True, null=True, default=None)
    canvas = models.FileField(verbose_name=_('canevas'), upload_to=upload_directory_file, blank=True, null=True, default=None)
    
    name = models.CharField(_('nom'), max_length=100)
    start_dt = DateField(_('du'))
    end_dt = DateField(_('au'))
    
    employee_direction = ModelSelect2Multiple('employee.direction', verbose_name=_('direction'), blank=True, help_text=leave_empty_for_all)
    employee_status = ModelSelect2Multiple('employee.status', verbose_name=_('status'), blank=True, help_text=leave_empty_for_all)
    employee_branch = ModelSelect2Multiple('employee.branch', verbose_name=_('site'), blank=True, help_text=leave_empty_for_all)
    employee_grade = ModelSelect2Multiple('employee.grade', verbose_name=_('grade'), blank=True, help_text=leave_empty_for_all)
    
    status = models.CharField(_('status'), max_length=25, choices=PayrollStatus, default=PayrollStatus.PROGRESS, editable=False)
    overall_net = models.FloatField(_('net global'), blank=True, default=0, editable=False)
    
    approvers = ModelSelect2Multiple('core.user', verbose_name=_('approbateurs'))
    approved = models.BooleanField(verbose_name=_('approuvé'), default=False)

    metadata = JSONField(verbose_name=_('meta'), default=_metadata, blank=True)
    
    list_display = ('id', 'name', 'start_dt', 'end_dt', 'overall_net', 'status', 'approved')
    list_filter = ('start_dt', 'end_dt')

    list_actions = [
        {
            "title": "Déclarations"
        }
    ]

    layout = Layout(
        'name',
        Column(
            FieldWithButtons(
                Field("canvas"), 
                StrictButton(
                    'Télécharger le modèle', 
                    css_class='btn btn-light-info', 
                    onclick="window.open('"+reverse_lazy('payroll:canvas')+"?status__in='+$('#id_employee_status').val().join(','), '_blank');"
                )
            )
        ),
        Row(Column('start_dt'), Column('end_dt')),
        Column(
            FieldWithButtons(
                Field("additional_items"), 
                StrictButton(
                    'Télécharger le modèle', 
                    css_class='btn btn-light-info', 
                    onclick="window.open('"+reverse_lazy('payroll:canvas-items-to-pay')+"?status__in='+$('#id_employee_status').val().join(','), '_blank');"
                )
            )
        ),
        Column('employee_status'),
        'metadata'
    )

    def get_absolute_url(self):
        return reverse_lazy('payroll:payslips', args=[self.pk])

    class Meta:
        verbose_name = _('paie')
        verbose_name_plural = _('paies')
