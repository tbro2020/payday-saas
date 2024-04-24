from django.utils.translation import gettext as _
from django.db import models

from core.models.fields import AceField, ModelSelect2Multiple
from crispy_forms.layout import Layout, Row, Column
from django.template import Context, Template
from core.models import Base

class BootstrapColumn(models.TextChoices):
    COL_1 = 'col-1', _('1/12')
    COL_2 = 'col-2', _('2/12')
    COL_3 = 'col-3', _('3/12')
    COL_4 = 'col-4', _('4/12')
    COL_5 = 'col-5', _('5/12')
    COL_6 = 'col-6', _('6/12')
    COL_7 = 'col-7', _('7/12')
    COL_8 = 'col-8', _('8/12')
    COL_9 = 'col-9', _('9/12')
    COL_10 = 'col-10', _('10/12')
    COL_11 = 'col-11', _('11/12')
    COL_12 = 'col-12', _('12/12')

class Widget(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100)
    column = models.CharField(verbose_name=_('column'), max_length=10, choices=BootstrapColumn.choices, default=BootstrapColumn.COL_12)

    permissions = ModelSelect2Multiple('auth.permission', verbose_name=_('permissions'))
    template = AceField(mode='html', verbose_name=_('template'))
    view = AceField(mode='python', verbose_name=_('view'))

    list_display = ('id', 'name', 'column', 'updated_at')
    layout = Layout(
        Row(
            Column('name', css_class='col-md-6'),
            Column('column', css_class='col-md-6'),
        ),
        'permissions',
        Row(
            Column('template', css_class='col-md-6'),
            Column('view', css_class='col-md-6'),
        ),
    )

    def render(self):
        template = Template(self.template)
        exec(self.view, globals(), locals())
        return template.render(Context(locals()))

    class Meta:
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')