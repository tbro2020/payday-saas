from django.utils.translation import gettext as _
from django.db import models
from crispy_forms.layout import Layout, Row, Column
from django.template import Context, Template

from core.models import fields, Base

class BootstrapColumn(models.TextChoices):
    COL_1 = 'col-md-1 col-xs-12', _('1/12')
    COL_2 = 'col-md-2 col-xs-12', _('2/12')
    COL_3 = 'col-md-3 col-xs-12', _('3/12')
    COL_4 = 'col-md-4 col-xs-12', _('4/12')
    COL_5 = 'col-md-5 col-xs-12', _('5/12')
    COL_6 = 'col-md-6 col-xs-12', _('6/12')
    COL_7 = 'col-md-7 col-xs-12', _('7/12')
    COL_8 = 'col-md-8 col-xs-12', _('8/12')
    COL_9 = 'col-md-9 col-xs-12', _('9/12')
    COL_10 = 'col-md-10 col-xs-12', _('10/12')
    COL_11 = 'col-md-11 col-xs-12', _('11/12')
    COL_12 = 'col-md-12 col-xs-12', _('12/12')

class Widget(Base):
    content_type = fields.ModelSelectField(
        'contenttypes.contenttype',
        verbose_name=_('type de contenu')
    )
    column = models.CharField(
        verbose_name=_('colonne'),
        max_length=30,
        choices=BootstrapColumn.choices,
        default=BootstrapColumn.COL_12
    )
    name = models.CharField(
        verbose_name=_('nom'),
        max_length=100
    )

    """
    permissions = fields.ModelSelect2Multiple(
        'core.permission',
        verbose_name=_('permissions'),
        blank=True
    )
    """

    template = fields.AceField(
        mode='html',
        verbose_name=_('modèle')
    )
    view = fields.AceField(
        mode='python',
        verbose_name=_('vue')
    )

    is_active = models.BooleanField(
        verbose_name=_('est actif'),
        default=True
    )

    list_display = ('id', 'name', 'column', 'updated_at')
    layout = Layout(
        Column('content_type'),
        Row(
            Column('name'),
            Column('column'),
        ),
        Row(
            Column('template'),
            Column('view'),
        )
    )

    def render(self, request=None):
        _locals = {}
        template = Template(self.template)
        exec(self.view, globals(), _locals)
        return template.render(Context(_locals))

    class Meta:
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')

from simple_history import register
register(Widget)