import glob
from .base import Base
from django.db import models
from .fields import ModelSelect2Multiple
from django.utils.translation import gettext as _

from crispy_forms.layout import Layout, Row, Column
from django.contrib.contenttypes.models import ContentType


class Menu(Base):
    ICONS = [((icon.split('/')[-1]).split('.')[0], ' '.join(((icon.split('/')[-1]).split('.')[0]).split('-')).title()) for icon in glob.glob("ICONS/*.svg")]

    icon = models.CharField(verbose_name=_('icon'), choices=ICONS, max_length=100, null=True, default=None)
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)
    children = ModelSelect2Multiple(ContentType, verbose_name=_('sous-menu'))
    
    layout = Layout(Row(Column('icon'), Column('name')), 'children')
    list_display = ('id', 'name', 'updated_at')
    search_fields = ('id', 'name')
    
    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')