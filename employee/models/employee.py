from employee.models.base import Employee as BaseEmployee
from crispy_forms.layout import Layout, Row, Column, Div
from django.utils.translation import gettext as _
from crispy_forms.bootstrap import PrependedText
from django.urls import reverse_lazy

from core.models import fields
from django.db import models
from django.apps import apps
from employee.utils import *

class Employee(BaseEmployee):
    user = fields.OneToOneField('core.user', verbose_name=_('utilisateur'), blank=True, null=True, on_delete=models.SET_NULL, default=None, editable=False)
    registration_number = fields.CharField(_('matricule'), max_length=50, unique=True, default=default_registration_number)
    email = fields.EmailField(_('email'), blank=True, null=True, default=None)

    list_display = ('registration_number', 'last_name', 'middle_name', 'branch', 'designation', 'grade', 'status')
    inlines = ['employee.child', 'employee.document', 'payroll.specialemployeeitem']

    layout = Layout(
        'photo',
        Row(
            Column('registration_number'),
            Column('social_security_number')
        ),
        Row(
            Column('agreement'),
            Column('date_of_join')
        ),
        Row(
            Column('direction', css_class="col-md-4"),
            Column('sub_direction', css_class="col-md-4"),
            Column('service', css_class="col-md-4"),
        ),
        Row(
            Column('branch'),
            Column('grade'),
            Column('designation'),
        ),
        Row(
            Column('first_name'),
            Column('middle_name'),
            Column('last_name'),
        ),
        Row(
            Column('date_of_birth'),
            Column('gender'),
        ),
        Row(
            Column('marital_status'),
            Column('spouse'),
            Column('spouse_date_of_birth')
        ),
        Row(
            Column(Div(PrependedText('mobile_number', '+', active=True))),
            Column('email'),
        ),
        Row(
            Column('physical_address'),
            Column('emergency_information'),
        ),
        Row(
            Column('payment_method'),
            Column('payer_name'),
            Column('payment_account'),
        ),
        'comment',
        'status'
    )

    def payslips(self):
        model = apps.get_model('payroll', 'payslip')
        return model.objects.filter(**{'employee__registration_number': self.registration_number})
    
    def attendances(self, period=None):
        return list()
    
    @property
    def actions_url(self):
        return [{
            'url': reverse_lazy('core:list', kwargs={'app': 'payroll', 'model': 'payslip'}) + '?employee__registration_number=' + self.registration_number,
            'title': _('bulletins de paie')
        }]
    
    def create_user(self):
        if not self.email: return
        if self.user: return self.user
        from django.contrib.auth import get_user_model
        
        user, created = get_user_model().objects.get_or_create(email=self.email)
        if created:
            from django.contrib.auth.models import Group
            from django.apps import apps
            
            preference = apps.get_model('core', 'preference')
            group = preference.get('DEFAULT_PERMISSION_GROUP')
            group = Group.objects.filter(name=group).first()
            if group: user.groups.add(group)

        self.user = user
        self.save()

    class Meta:
        verbose_name = _('employé')
        verbose_name_plural = _('employés')