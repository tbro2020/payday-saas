from django.utils.translation import gettext as _
from .sub_direction import SubDirection

from crispy_forms.layout import Layout, Row, Column
from django.db import models

from core.models import fields
from core.models import Base

class Service(Base):
    sub_direction = fields.ModelSelectField(SubDirection, verbose_name=_('sous-direction'), on_delete=models.CASCADE)
    number_of_employee = fields.IntegerField(verbose_name=_('nombre d\'employés prévus'), default=1)
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    search_fields = ('sub_direction__name', 'name')
    list_display = ('id', 'subdirection', 'name')
    list_filter = ('sub_direction',)
    
    layout = Layout(
        Row(
            Column('sub_direction'),
            Column('name')
        ),
        'number_of_employee',
    )
    inline_form_fields = ('name',)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
