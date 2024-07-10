from crispy_forms.layout import Layout, Row, Column, Div, Fieldset
from phonenumber_field.modelfields import PhoneNumberField

from crispy_forms.bootstrap import PrependedText
from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from core.models.fields import DateField
from django.urls import reverse_lazy
from django.db import models
from django.apps import apps

from .position import Position
from .agreement import Agreement
from .grade import Grade

from .sub_direction import SubDirection
from .direction import Direction
from .service import Service

from core.models import Base
from datetime import date

from employee.models.managers import EmployeeQuerySet
from random import randint

default_photo = lambda: "place_pics/default_pic.jpg"
#default_registration_number = lambda: randint(100000000, 999999999)


class Employee(Base):
    PAYMENT_METHODS = (('cash', _('Cash')), ('bank', _('Bank')), ('mobile Money', _('Mobile Money')))
    MARITAL_STATUS = (('married', _('Marié')), ('widower', _('Veuf')), ('single', _('Célibataire')))
    GENDERS = (('male', _('Homme')), ('female', _('Femme')))

    registration_number = models.CharField(_('matricule'), max_length=50, unique=True, db_index=True, primary_key=True)
    social_security_number = models.CharField(_('numéro de sécurité sociale'), max_length=50, blank=True, null=True, default=None)
    
    agreement = ModelSelect(Agreement, verbose_name=_('type de contrat'), blank=True, null=True, on_delete=models.SET_NULL)
    date_of_join = DateField(_('date d\'engagement'), null=True, default=None)
    photo = models.ImageField(_('photo'), blank=True, null=True)

    position = ModelSelect('employee.Position', verbose_name=_('position'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = ModelSelect('employee.grade', verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)
    branch = ModelSelect('employee.Branch', verbose_name=_('site'),  null=True, on_delete=models.SET_NULL)
    

    direction = ModelSelect(Direction, verbose_name=_('direction'), null=True, on_delete=models.SET_NULL, default=None)
    sub_direction = ModelSelect(SubDirection, verbose_name=_('sous-direction'), blank=True, null=True, on_delete=models.SET_NULL, default=None)
    service = ModelSelect(Service, verbose_name=_('service'), blank=True, null=True, on_delete=models.SET_NULL, default=None)

    middle_name = models.CharField(_('post-nom'), max_length=100, blank=True, null=True, default=None)
    first_name = models.CharField(_('prénom'), max_length=100, blank=True, null=True, default=None)
    last_name = models.CharField(_('nom'), max_length=100, blank=True, null=True, default=None)

    date_of_birth = DateField(_('date de naissance'), null=True, default=None)
    gender = models.CharField(_('genre'), max_length=10, choices=GENDERS)

    marital_status = models.CharField(_('état civil'), max_length=12, choices=MARITAL_STATUS)
    spouse = models.CharField(_('conjoint'), max_length=100, blank=True, null=True, default=None)

    mobile_number = PhoneNumberField(_('numéro de téléphone mobile'), null=True, default=None)
    email = models.EmailField(_('email'), blank=True, null=True, default=None)

    physical_address = models.TextField(_('adresse physique'), null=True, default=None)
    emergency_information = models.TextField(_('informations d\'urgence'), null=True, default=None)

    payer = ModelSelect('employee.payer', verbose_name=_('banque'), null=True, on_delete=models.SET_NULL, default=None)
    payment_account = models.CharField(_('numéro de compte'), max_length=50, blank=True, null=True, default=None)
    payment_method = models.CharField(_('mode de paiement'), max_length=20, choices=PAYMENT_METHODS)

    comment = models.TextField(_('commentaire'), blank=True, null=True, default=None)
    status = ModelSelect('employee.Status', verbose_name=_('code d\'activité'), null=True, on_delete=models.SET_NULL, default=None)

    objects = EmployeeQuerySet()

    list_filter = ('grade', 'direction', 'branch', 'position', 'status', 'date_of_join', 'date_of_birth')
    list_display = ('registration_number', 'grade', 'branch', 'last_name', 'middle_name', 'status')
    search_fields = ('registration_number', )

    inlines = ['employee.child', 'employee.education', 'employee.experience', 'employee.document', 'payroll.specialemployeeitem']

    layout = Layout(
        'photo',
        Row(
            Column('registration_number', css_class='col-md-6 col-sm-12'),
            Column('social_security_number', css_class='col-md-6 col-sm-12')
        ),
        Row(
            Column('branch', css_class='col-md-4 col-sm-12'),
            Column('agreement', css_class='col-md-4 col-sm-12'),
            Column('date_of_join', css_class='col-md-4 col-sm-12')
        ),
        Row(
            Column('direction', css_class='col-md-4 col-sm-12'),
            Column('sub_direction', css_class='col-md-4 col-sm-12'),
            Column('service', css_class='col-md-4 col-sm-12'),
        ),
        Row(
            Column('grade', css_class='col-md-6 col-sm-12'),
            Column('position', css_class='col-md-6 col-sm-12'),
        ),
        Row(
            Column('first_name', css_class='col-md-4 col-sm-12'),
            Column('middle_name', css_class='col-md-4 col-sm-12'),
            Column('last_name', css_class='col-md-4 col-sm-12'),
        ),
        Row(
            Column('date_of_birth', css_class='col-md-6 col-sm-12'),
            Column('gender', css_class='col-md-6 col-sm-12'),
        ),
        Row(
            Column('marital_status', css_class='col-md-6 col-sm-12'),
            Column('spouse', css_class='col-md-6 col-sm-12'),
        ),
        Row(
            Div(PrependedText('email', '@', active=True), css_class='col-md-6 col-sm-12'),
            Div(PrependedText('mobile_number', '+', active=True), css_class='col-md-6 col-sm-12')
        ),
        Row(
            Column('physical_address', css_class='col-md-6 col-sm-12'),
            Column('emergency_information', css_class='col-md-6 col-sm-12'),
        ),
        Row(
            Column('payment_method', css_class='col-md-4 col-sm-12'),
            Column('payer', css_class='col-md-4 col-sm-12'),
            Column('payment_account', css_class='col-md-4 col-sm-12'),
        ),
        'comment',
        'status',
        Fieldset(
            'Information supplémentaire',
            'metadata',
            css_class='mt-5 bg-light-warning p-3 rounded'
        )
    )

    def full_name(self):
        return f"{self.registration_number} / {self.last_name} {self.middle_name}, {self.first_name}"
    
    def short_name(self):
        return f"{self.registration_number} /  {self.last_name} {self.middle_name}"

    @property
    def name(self):
        return self.short_name()
    
    def get_absolute_url(self):
        return reverse_lazy("employee:change", kwargs={"pk": self.registration_number})
    
    # To Do : Improve this method to filter according to range of period
    def attendances(self, period=None):
        period = period if period else date.today()
        Attendance = apps.get_model('employee', model_name='attendance')
        attendances = Attendance.objects.filter(employee=self)
        attendances = attendances.filter(employee=self, date__year=period.year)
        attendances = attendances.filter(direction='OUT').values('employee', 'date')
        return list(attendances.values('date').annotate(count=models.Count('employee')))
    
    def attendances_by_range(self, start, end):
        Attendance = apps.get_model('employee', model_name='attendance')
        attendances = Attendance.objects.filter(employee=self)
        attendances = attendances.filter(employee=self, date__range=[start, end])
        attendances = attendances.filter(direction='OUT').values('employee', 'date')
        return list(attendances.values('date').annotate(count=models.Count('employee')))
    
    def get_or_create_user(self):
        if not self.email: return
        from django.contrib.auth import get_user_model
        if user:= get_user_model().objects.filter(email=self.email).first():
            return user
        return get_user_model().objects.create(employee=self, email=self.email)

    class Meta:
        verbose_name = _('employé')
        verbose_name_plural = _('employés')
        ordering = ('-status', 'registration_number')