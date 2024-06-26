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
            ),
            css_class='col-md-12 col-sm-12'
        ),
        Row(Column('start_dt', css_class='col-md-6 col-sm-12'), Column('end_dt', css_class='col-md-6 col-sm-12')),
        Column(
            FieldWithButtons(
                Field("additional_items"), 
                StrictButton(
                    'Télécharger le modèle', 
                    css_class='btn btn-light-info', 
                    onclick="window.open('"+reverse_lazy('payroll:canvas-items-to-pay')+"?status__in='+$('#id_employee_status').val().join(','), '_blank');"
                )
            ),
            css_class='col-md-12 col-sm-12'
        ),
        Column('employee_status', css_class='col-md-12 col-sm-12'),
        'metadata'
    )

    def get_absolute_url(self):
        return reverse_lazy('payroll:payslips', args=[self.pk])
    
    def statistic(self):
        import pandas as pd
        from django.apps import apps
        payslips = self.payslip_set.all()
        items_paid = apps.get_model('payroll', 'itempaid').objects.filter(payslip__payroll=self)

        legals = apps.get_model('payroll', 'legalitem').objects.values_list('code', flat=True)
        impact = payslips.values('_employee__status__name').annotate(count=models.Count('_employee__status__name'), net=models.Sum('net'))
        legals = items_paid.filter(code__in=legals).values('name').annotate(amount=models.Sum(models.Func(models.F('amount_qp_employee') + models.F('amount_qp_employer'), function='ABS')))

        impact = pd.DataFrame(list(impact))
        impact['net_usd'] = round(impact['net'] / self.metadata.get('taux', 2800), 2)
        impact = impact.append(impact.sum(numeric_only=True), ignore_index=True)

        impact = impact.to_html(index=False, classes='table table-striped mt-3')
        impact = impact.replace('<th>', '<th style="text-align: left;" class="text-capitalize">')
        
        legals = pd.DataFrame(list(legals))
        legals['amount_usd'] = round(legals['amount'] / self.metadata.get('taux', 2800), 2)
        legals = legals.append(legals.sum(numeric_only=True), ignore_index=True)

        legals = legals.to_html(index=False, classes='table table-striped mt-3')
        legals = legals.replace('<th>', '<th style="text-align: left;" class="text-capitalize">')

        return {
            'deductibles': round(abs(items_paid.filter(amount_qp_employee__lte=0).aggregate(amount=models.Sum('amount_qp_employee')).get('amount', 0)), 2),
            'gross': round(abs(items_paid.filter(amount_qp_employee__gte=0).aggregate(amount=models.Sum('amount_qp_employee')).get('amount', 0)), 2),
            'net': self.overall_net,
            'payslips': payslips,

            'branches': payslips.values_list('_employee__branch__name', flat=True).distinct(),
            'statues': payslips.values_list('_employee__status__name', flat=True).distinct(),
            'branks': payslips.values_list('_employee__payer__name', flat=True).distinct(),
            
            'impact': impact,
            'legals': legals
        }

    class Meta:
        verbose_name = _('paie')
        verbose_name_plural = _('paies')
