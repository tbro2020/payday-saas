from phonenumber_field.modelfields import PhoneNumberField
from crispy_forms.layout import Layout, Row, Column, Div
from django.utils.translation import gettext as _
from crispy_forms.bootstrap import PrependedText

from django.urls import reverse_lazy
from django.apps import apps
from django.db import models

from .designation import Designation
from .agreement import Agreement
from .grade import Grade

from .sub_direction import SubDirection
from .direction import Direction
from .service import Service

from core.utils import upload_directory_file
from core.models import Base, fields
from datetime import date

default_registration_number = lambda: "0000000000"

class Employee(Base):
    GENDERS = (('Male', _('Homme')), ('Female', _('Femme')))

    MARITAl_STATUS = (('Maried', _('Marié')), ('Single', _('Célibataire')), ('Widower', _('Veuf')))
    PAYMENT_METHODS = (('Cash', _('Cash')), ('Bank', _('Bank')), ('Mobile Money', _('Mobile Money')))

    registration_number = fields.CharField(_('matricule'), max_length=50, unique=True, default=default_registration_number)
    social_security_number = fields.CharField(_('numéro de sécurité sociale'), max_length=50, blank=True, null=True, default=None)
    
    agreement = fields.ModelSelectField(Agreement, verbose_name=_('type de contrat'), on_delete=models.CASCADE)
    date_of_join = fields.DateField(_('date d\'engagement'), help_text='YYYY-MM-DD', null=True, default=None)
    photo = fields.ImageField(_('photo'), upload_to=upload_directory_file, blank=True, null=True)

    designation = fields.ModelSelectField(Designation, verbose_name=_('position'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = fields.ModelSelectField(Grade, verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)

    direction = fields.ModelSelectField(Direction, verbose_name=_('direction'), null=True, on_delete=models.SET_NULL, default=None)
    sub_direction = fields.ModelSelectField(SubDirection, verbose_name=_('sous-direction'), blank=True, null=True, on_delete=models.SET_NULL, default=None)
    service = fields.ModelSelectField(Service, verbose_name=_('service'), blank=True, null=True, on_delete=models.SET_NULL, default=None)

    middle_name = fields.CharField(_('post-nom'), max_length=100, blank=True, null=True, default=None)
    first_name = fields.CharField(_('prénom'), max_length=100, blank=True, null=True, default=None)
    last_name = fields.CharField(_('nom'), max_length=100, blank=True, null=True, default=None)

    date_of_birth = fields.DateField(_('date de naissance'), help_text='YYYY-MM-DD', null=True, default=None)
    gender = fields.CharField(_('genre'), max_length=10, choices=GENDERS)

    spouse_date_of_birth = fields.DateField(_('date de naissance du conjoint'), help_text='YYYY-MM-DD', blank=True, null=True, default=None)
    spouse = fields.CharField(_('conjoint'), max_length=100, blank=True, null=True, default=None)
    marital_status = fields.CharField(_('état civil'), max_length=12, choices=MARITAl_STATUS)

    mobile_number = PhoneNumberField(_('numéro de téléphone mobile'), null=True, default=None)
    physical_address = fields.TextField(_('adresse physique'), blank=True, null=True, default=None)
    emergency_information = fields.TextField(_('informations d\'urgence'), null=True, default=None)

    syndicate = fields.ModelSelectField('employee.Syndicate', verbose_name=_('syndicat'),  blank=True, null=True, on_delete=models.SET_NULL)
    branch = fields.ModelSelectField('employee.Branch', verbose_name=_('site'),  null=True, on_delete=models.SET_NULL)

    payment_method = fields.CharField(_('mode de paiement'), max_length=20, choices=PAYMENT_METHODS)
    payer_name = fields.CharField(_('nom du payeur'), max_length=50, null=True, default=None)
    pay_account = fields.CharField(_('numéro de compte'), max_length=50, blank=True, null=True, default=None)

    comment = fields.TextField(_('commentaire'), blank=True, null=True, default=None)
    status = fields.ModelSelectField('employee.Status', verbose_name=_('status'), null=True, on_delete=models.SET_NULL, default=None)

    list_filter = ('agreement', 'date_of_join', 'direction', 'branch', 'designation', 'gender', 'marital_status', 'branch', 'status')
    search_fields = ('registration_number', 'social_security_number', 'agreement__name',
                    'designation__name', 'grade__name', 'direction__name', 'sub_direction__name',
                    'service__name', 'first_name', 'middle_name', 'last_name', 'spouse',
                    'mobile_number', 'physical_address', 'emergency_information',
                    'branch__name', 'syndicate__name', 'pay_account', 'comment')
    list_display = ('registration_number', 'last_name', 'middle_name', 'designation', 'branch')

    inlines = ['employee.child', 'employee.document']

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
            Column('grade'),
            Column('designation')
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
        Div(PrependedText('mobile_number', '+', active=True)),
        Row(
            Column('physical_address'),
            Column('emergency_information'),
        ),
        Row(
            Column('branch'),
            Column('syndicate'),
        ),
        Row(
            Column('payment_method'),
            Column('payer_name'),
            Column('pay_account'),
        ),
        'comment',
        'status'
    )

    _layout = layout

    def full_name(self):
        return f"{self.registration_number} / {self.last_name} {self.middle_name}, {self.first_name}"
    
    def short_name(self):
        return f"{self.registration_number} / {self.last_name} {self.first_name}"

    @property
    def name(self):
        return self.short_name()
    
    def is_retired(self):
        return self.status.name == 'Retired'
    
    def get_absolute_url(self):
        return reverse_lazy("employee:change", kwargs={"pk": self.pk})
    
    def attendances(self, period=None):
        period = period if period else date.today()
        Attendance = apps.get_model('employee', model_name='attendance')
        attendances = Attendance.objects.filter(employee=self)
        attendances = attendances.filter(employee=self, date__year=period.year)
        attendances = attendances.filter(direction='OUT').values('employee', 'date')
        attendances = attendances.values('date').annotate(count=models.Count('employee'))
        return list(attendances)
    
    def create_user(self):
        if not self.email: return
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if user:= User.objects.filter(email=self.email).first(): 
            return user
        return User.objects.create(employee=self, email=self.email)

    class Meta:
        verbose_name = _('employé')
        verbose_name_plural = _('employés')