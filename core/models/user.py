from crispy_forms.layout import Layout, Row, Column
from django.urls import reverse_lazy
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from core.models import managers
from core.models import fields


class User(AbstractUser):
    organization = fields.ModelSelectField('core.organization', verbose_name=_('organisation'), on_delete=models.SET_NULL, null=True, blank=True, default=None, editable=False)
    
    updated_at = fields.DateTimeField(verbose_name=_('mis à jour le/à'), auto_now=True)
    created_at = fields.DateTimeField(verbose_name=_('créé le/à'), auto_now_add=True)
    first_name, last_name, username = None, None, None

    user_permissions = fields.ModelSelect2Multiple('auth.permission', verbose_name=_('permissions'), blank=True)
    groups = fields.ModelSelect2Multiple('auth.group', verbose_name=_('groupes'), blank=True)
    
    email = fields.EmailField(unique=True, db_index=True, verbose_name=_('email'))
    password = fields.CharField(_('mot de passe'), max_length=128, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()
    
    list_display = ('id', 'email', 'is_active')
    search_fields = ('id', 'email',)
    list_filter = ('is_active',)
    
    layout = Layout(
        Row(
            Column('organization'),
            Column('email')
        ),
        Row(
            Column('user_permissions'),
            Column('groups')
        ),
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

    def get_absolute_url(self):
        meta = self._meta
        return reverse_lazy('core:change', kwargs={'app': meta.app_label, 'model': meta.model_name, 'pk': self.pk})