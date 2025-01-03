from django_currentuser.db.models import CurrentUserField
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from autoslug import AutoSlugField
from django.db import models

from core.models import fields
from core.utils import upload_directory_file

slugify = lambda value: value.replace(' ', '_').lower()
default_logo = lambda: "assets/images/logo/logo.svg"

class Organization(models.Model):
    updated_by = CurrentUserField(
        verbose_name=_('mis à jour par'),
        related_name='%(app_label)s_%(class)s_updated_by',
        on_update=True
    )
    created_by = CurrentUserField(
        verbose_name=_('créé par'),
        related_name='%(app_label)s_%(class)s_created_by'
    )

    updated_at = fields.DateTimeField(
        verbose_name=_('mis à jour le/à'),
        auto_now=True
    )
    created_at = fields.DateTimeField(
        verbose_name=_('créé le/à'),
        auto_now_add=True
    )

    logo = fields.ImageField(
        verbose_name=_('logo'),
        upload_to=upload_directory_file,
        default=default_logo()
    )
    subdomain_prefix = AutoSlugField(
        populate_from='name',
        unique=True,
        editable=False
    )
    name = fields.CharField(
        verbose_name=_('nom'),
        max_length=100
    )
    
    list_display = ('name', 'national_id', 'commercial_register_number')
    layout = Layout('name', 'subdomain_prefix', 'logo')
    search_fields = ('name', 'national_id')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = _('organizations')
        verbose_name = _('organization')
