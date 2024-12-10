from django_currentuser.db.models import CurrentUserField
from django.utils.translation import gettext as _
from core.utils import upload_directory_file
from crispy_forms.layout import Layout
from autoslug import AutoSlugField

from core.models import fields
from django.db import models

slugify = lambda value: value.replace(' ','_').lower()
default_logo = lambda: "assets/images/logo/logo.svg"

class Organization(models.Model):
    updated_by = CurrentUserField(verbose_name=_('mis à jour par') ,related_name='%(app_label)s_%(class)s_updated_by', on_update=True)
    created_by = CurrentUserField(verbose_name=_('créé par') ,related_name='%(app_label)s_%(class)s_created_by')

    updated_at = fields.DateTimeField(verbose_name=_('mis à jour le/à'), auto_now=True)
    created_at = fields.DateTimeField(verbose_name=_('créé le/à'), auto_now_add=True)
    
    metadata = fields.JSONField(verbose_name=_('meta'), default=dict, blank=True)

    logo = fields.ImageField(verbose_name=_('logo'), upload_to=upload_directory_file, default=default_logo())
    subdomain_prefix = AutoSlugField(populate_from='name', unique=True, editable=False)
    name = fields.CharField(verbose_name=_('nom'), max_length=100)
    
    list_display = ('name', 'national_id', 'commercial_register_number')
    search_fields = ('name', 'national_id')
    layout = Layout('name', 'logo')

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __str__(self) -> str:
        return self.name