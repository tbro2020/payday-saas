from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from .fields import ModelSelect, AceField
from tinymce.models import HTMLField

from django.db import models
from .base import Base

class Template(Base):
    content = HTMLField(_('contenu'), null=True, default=None)
    name = models.CharField(_('nom'), max_length=100, unique=True)
    condition = AceField(_('condition'), default='1', help_text=_('condition d\'affichage du modèle'))
    content_type = ModelSelect(ContentType, verbose_name=_('type de contenu'), on_delete=models.CASCADE)
    
    
    search_field = ('name')
    list_display = ('id', 'content_type', 'name')
    layout = Layout(Row(Column('content_type'), Column('name')), 'content')

    class Meta:
        verbose_name = _('modèle de document')
        verbose_name_plural = _('modèles de documents')