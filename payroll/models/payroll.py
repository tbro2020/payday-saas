from crispy_forms.layout import Layout, Row, Column, Fieldset
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db import models

from core.models.fields import ModelSelect2Multiple
from core.models.fields import DateField, JSONField
from core.models import Base
from functools import reduce
from django.apps import apps

leave_empty_for_all = _('laisser vide pour tous')

class PayrollStatus(models.TextChoices):
    WARNING = ('WARNING', _('avertissement'))
    PROGRESS = ('PROGRESS', _('en cours'))
    SUCCESS = ('SUCCESS', _('succès'))

class Payroll(Base):

    def _metadata():
        return dict(taux_usd_cdf=2000)

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
        #'approvers',
        Row(Column('start_dt'), Column('end_dt')),
        #Fieldset(
        #    _('Employees'),
        #    Row(
        #        Column('employee_direction'), 
        #        Column('employee_branch'), 
        #        Column('employee_grade')
        #    ), 
        #    Column('employee_status'),
        #    css_class='mt-5 mb-5'
        #),
        Column('employee_status'),
        'metadata'
    )

    
    def get_absolute_url(self):
        return reverse_lazy('payroll:payslips', args=[self.pk])
    
    def sheet(self):
        rows = []
        Employee = apps.get_model('employee', model_name='employee')
        
        employee_list_display = ['registration_number', 'social_security_number', 'first_name', 'middle_name', 'last_name']
        employee_list_display = [field for field in Employee._meta.fields if field.name in employee_list_display]
        employee_list_display = employee_list_display + [field for field in Employee._meta.fields if field.choices or field.get_internal_type() == 'ModelSelect']
        
        payslips = self.payslip_set.all().select_related().prefetch_related()
        items = [payslip.itempaid_set.all().values('name').distinct() for payslip in payslips]
        items = [[i['name'] for i in item] for item in items]
        items = reduce(lambda x,y:x+y,items)
        items = list(set(items))
        
        for payslip in payslips:
            row = {field.verbose_name.title(): str(getattr(payslip.employee, field.name, "Null")) for field in employee_list_display}
            for item in items: row[item.title()] = 0
            for item in payslip.itempaid_set.all().order_by('code'):
                row[item.name.title()] = item.amount_qp_employee
            payslip_list_display = (field for field in payslip._meta.model._meta.fields if field.get_internal_type() == 'FloatField')
            row.update({field.verbose_name.title(): getattr(payslip, field.name) for field in payslip_list_display})
            rows.append(row)
        return rows

    class Meta:
        verbose_name = _('paie')
        verbose_name_plural = _('paies')
