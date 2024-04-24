from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from django.db import models

from core.models import Base


class TypeOfLeave(Base):
    name = models.CharField(_('nom'), max_length=100)
    max_days_per_year = models.IntegerField(_('Nombre maximal de jours par an'))

    layout = Layout(Row(Column('name'), Column('max_days_per_year')))
    list_display = ('id', 'name', 'max_days_per_year')
    search_fields = ('name',)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('type de congé')
        verbose_name_plural = _('type de congé')
