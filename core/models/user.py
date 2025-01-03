from crispy_forms.layout import Layout, Row, Column
from django.urls import reverse_lazy

from django.contrib.auth.models import AbstractBaseUser
from core.models.mixins import PermissionsMixin
from django.utils.translation import gettext as _
from django.db.models import Q
from django.db import models

from core.models.managers import UserManager
from core.models import fields
from django.apps import apps

from functools import reduce
from operator import or_

class User(AbstractBaseUser, PermissionsMixin):
    first_name, last_name, username = None, None, None

    organization = fields.ModelSelectField(
        'core.organization', 
        verbose_name=_('organisation'), 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        default=None, 
        editable=False
    )
    
    updated_at = fields.DateTimeField(
        verbose_name=_('mis à jour le/à'), 
        auto_now=True
    )
    created_at = fields.DateTimeField(
        verbose_name=_('créé le/à'), 
        auto_now_add=True
    )

    email = fields.EmailField(
        unique=True, 
        db_index=True, 
        verbose_name=_('email')
    )
    password = fields.CharField(
        verbose_name=_('mot de passe'), 
        max_length=128, 
        blank=True
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        )
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()
    
    inlines = ('core.permission', 'core.rowlevelsecurity',)
    list_display = ('id', 'email', 'is_active')
    search_fields = ('id', 'email',)
    list_filter = ('is_active',)
    
    layout = Layout(
        Column('email'),
        Column('roles'),
        Row(
            Column('is_staff'),
            Column('is_active'),
            Column('is_superuser')
        )
    )

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.email

    def get_full_name(self):
        return self.name
    
    def notify(self, _from, subject, message, *args, **kwargs):
        notification = apps.get_model('core', 'notification')
        return notification.objects.create(_from=_from, _to=self, subject=subject, message=message)
    
    def get_user_rls(self, app, model, *args, **kwargs):
        if self.is_superuser:
            return {}
        
        rowlevelsecurity = apps.get_model('core', 'rowlevelsecurity')
        roles = self.roles.all().values_list('id', flat=True)
        rls = rowlevelsecurity.objects.filter(
            content_type__app_label = app,
            content_type__model = model
        ).filter(Q(role__id__in=roles) | Q(user=self))\
            .filter(*args, **kwargs).values('field', 'value')
        return {item['field']: item['value'] for item in rls}

    def get_absolute_url(self):
        return reverse_lazy(
            'core:change', 
            kwargs={'app': self._meta.app_label, 'model': self._meta.model_name, 'pk': self.pk}
        )

from simple_history import register
register(User)
