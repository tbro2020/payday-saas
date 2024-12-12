from phonenumber_field.modelfields import PhoneNumberField
from crispy_forms.layout import Layout, Row, Column, Div
from django.utils.translation import gettext as _
from crispy_forms.bootstrap import PrependedText

from django.urls import reverse_lazy
from django.db import models

from core.utils import upload_directory_file
from core.models import Base, fields
from employee.utils import *

PAYMENT_METHODS = (('cash', _('cash')), ('bank', _('bank')), ('mobile Money', _('mobile Money')))
MARITAl_STATUS = (('maried', _('marié')), ('single', _('célibataire')), ('widower', _('veuf')))
GENDERS = (('male', _('homme')), ('female', _('femme')))

class Employee(Base):
    social_security_number = fields.CharField(_('numéro de sécurité sociale'), max_length=50, blank=True, null=True, default=None)
    registration_number = fields.CharField(_('matricule'), max_length=50)

    agreement = fields.ModelSelectField('employee.agreement', verbose_name=_('type de contrat'), on_delete=models.CASCADE)
    date_of_join = fields.DateField(_('date d\'engagement'), help_text='YYYY-MM-DD', null=True, default=None)
    photo = fields.CaptureField(_('photo'), upload_to=upload_directory_file, blank=True, null=True)

    designation = fields.ModelSelectField('employee.designation', verbose_name=_('position'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = fields.ModelSelectField('employee.grade', verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)

    sub_direction = fields.ModelSelectField('employee.subdirection', verbose_name=_('sous-direction'), blank=True, null=True, on_delete=models.SET_NULL, default=None)
    service = fields.ModelSelectField('employee.service', verbose_name=_('service'), blank=True, null=True, on_delete=models.SET_NULL, default=None)
    direction = fields.ModelSelectField('employee.direction', verbose_name=_('direction'), null=True, on_delete=models.SET_NULL, default=None)

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

    branch = fields.ModelSelectField('employee.Branch', verbose_name=_('site'),  null=True, on_delete=models.SET_NULL)

    payment_account = fields.CharField(_('numéro de compte/paiement'), max_length=50, blank=True, null=True, default=None)
    payment_method = fields.CharField(_('mode de paiement'), max_length=20, choices=PAYMENT_METHODS)
    payer_name = fields.CharField(_('nom du payeur'), max_length=50, null=True, default=None)

    comment = fields.TextField(_('commentaire'), blank=True, null=True, default=None)
    status = fields.ModelSelectField('employee.status', verbose_name=_('status'), null=True, on_delete=models.SET_NULL, default=None)

    list_filter = ('agreement', 'date_of_join', 'direction', 'branch', 'designation', 'gender', 'marital_status', 'branch', 'status')
    search_fields = ('registration_number', 'social_security_number', 'agreement__name',
                    'designation__name', 'grade__name', 'direction__name', 'sub_direction__name',
                    'service__name', 'first_name', 'middle_name', 'last_name', 'spouse',
                    'mobile_number', 'physical_address', 'emergency_information',
                    'branch__name', 'payment_account', 'comment')
    list_display = ('registration_number', 'last_name', 'middle_name', 'designation', 'branch', 'status')

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
        Div(PrependedText('mobile_number', '+', active=True)),
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

    def full_name(self):
        return f"{self.registration_number} / {self.last_name} {self.middle_name}, {self.first_name}"
    
    def short_name(self):
        return f"{self.registration_number} / {self.last_name}"

    @property
    def name(self):
        return self.short_name()
    
    def get_absolute_url(self):
        return reverse_lazy("employee:change", kwargs={"pk": self.pk})

    class Meta:
        abstract = True
        verbose_name = _('employé')
        verbose_name_plural = _('employés')