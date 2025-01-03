from django.utils.translation import gettext as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Layout, Row, Column

from core.models import fields, Base
from .fields import ModelSelect2Multiple
import glob

class Menu(Base):
    ICONS = [
        ((icon.split('/')[-1]).split('.')[0], ' '.join(((icon.split('/')[-1]).split('.')[0]).split('-')).title()) 
        for icon in glob.glob("ICONS/*.svg")
    ]

    icon = fields.ChoiceField(
        verbose_name=_('icon'), 
        choices=ICONS, 
        max_length=100, 
        null=True, 
        default=None
    )
    children = fields.ModelSelect2Multiple(
        ContentType, 
        verbose_name=_('sous-menu')
    )
    name = fields.CharField(
        verbose_name=_('nom'), 
        max_length=100, 
        unique=True
    )

    layout = Layout(
        Row(Column('icon'), Column('name')), 
        'children'
    )
    list_display = ('id', 'name', 'updated_at')
    search_fields = ('id', 'name')

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
