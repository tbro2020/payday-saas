from crispy_forms.layout import Layout, Row, Column, Fieldset
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db import models


from core.models.fields import ModelSelect2Multiple
from core.models.fields import DateField
from core.models import Base

from employee.models import *
from functools import reduce

leave_empty_for_all = _('laisser vide pour tous')

class Payroll(Base):
    STATUS = (
        ('SUCCESS', _('succès')),
        ('WARNING', _('avertissement')),
        ('PROGRESS', _('en cours'))
    )

    METADATA = dict({'employee': {}, 'leave': {}, 'payroll': {}})

    name = models.CharField(_('nom'), max_length=100)
    start_dt = DateField(_('du'))
    end_dt = DateField(_('au'))
    
    direction = ModelSelect2Multiple(Direction, verbose_name=_('direction'), blank=True, help_text=leave_empty_for_all)
    branch = ModelSelect2Multiple(Branch, verbose_name=_('site'), blank=True, help_text=leave_empty_for_all)
    grade = ModelSelect2Multiple(Grade, verbose_name=_('grade'), blank=True, help_text=leave_empty_for_all)
    
    status = models.CharField(_('status'), max_length=25, choices=STATUS, default=STATUS[2][0], editable=False)
    overall_net = models.FloatField(_('net global'), blank=True, default=0, editable=False)
    
    list_display = ('id', 'name', 'start_dt', 'end_dt', 'overall_net', 'status')
    list_filter = ('start_dt', 'end_dt')

    layout = Layout(
        'name',
        Row(Column('start_dt'), Column('end_dt')),
        Fieldset(_('Employees'), Row(Column('direction', css_class='col-4'), Column('branch', css_class='col-4'), Column('grade', css_class='col-4')), css_class='mt-5'),
        'metadata'
    )

    
    def get_absolute_url(self):
        return reverse_lazy('payroll:payslips', args=[self.pk])
    
    def sheet(self):
        rows = []
        
        employee_list_display = ['registration_number', 'social_security_number', 'first_name', 'middle_name', 'last_name']
        employee_list_display = [field for field in Employee._meta.fields if field.name in employee_list_display]
        employee_list_display = employee_list_display + [field for field in Employee._meta.fields if field.name == 'payer_name' or
                                                                                                     field.choices or field.get_internal_type() == 'ModelSelect']
        
        payslips = self.payslip_set.all()
        items = [payslip.payitem_set.all().values('name').distinct() for payslip in payslips]
        items = [[i['name'] for i in item] for item in items]
        items = reduce(lambda x,y:x+y,items)
        items = list(set(items))
        
        for payslip in payslips:
            row = {field.verbose_name.title(): str(getattr(payslip.employee, field.name, "Null")) for field in employee_list_display}
            for item in items: row[item.title()] = 0
            for item in payslip.payitem_set.all().order_by('code'):
                row[item.name.title()] = item.amount
            payslip_list_display = (field for field in payslip._meta.model._meta.fields if field.get_internal_type() == 'FloatField')
            row.update({field.verbose_name.title(): getattr(payslip, field.name) for field in payslip_list_display})
            rows.append(row)
        return rows

    class Meta:
        verbose_name = _('paie')
        verbose_name_plural = _('paies')
