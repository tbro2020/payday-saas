from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _

from core.models import fields
from django.db import models
from .base import Base

class Template(Base):
    content_type = fields.ModelSelectField(ContentType, verbose_name=_('type de contenu'), on_delete=models.CASCADE)
    content = fields.HTMLField(_('contenu'), null=True, default=None)
    name = fields.CharField(_('nom'), max_length=100, unique=True)
    
    layout = Layout(Row(Column('content_type'), Column('name')), 'content')
    list_display = ('id', 'content_type', 'name')
    search_field = ('name')

    class Meta:
        verbose_name = _('modèle de document')
        verbose_name_plural = _('modèles de documents')