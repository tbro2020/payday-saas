from django.utils.translation import gettext as _
from core.models.fields import ModelSelect
from .sub_direction import SubDirection
from crispy_forms.layout import Layout, Row, Column
from core.models import Base
from django.db import models

class Service(Base):
    sub_direction = ModelSelect(SubDirection, verbose_name=_('sous-direction'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    search_fields = ('sub_direction__name', 'name')
    list_display = ('id', 'sub_direction', 'name')
    list_filter = ('sub_direction',)
    
    layout = Layout(
        Row(
            Column('sub_direction'),
            Column('name')
        )
    )
    inline_form_fields = ('name',)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
