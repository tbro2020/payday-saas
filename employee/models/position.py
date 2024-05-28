from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Position(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100)

    layout = Layout('name')
    search_fields = ('name')
    list_display = ('id', 'name')

    class Meta:
        verbose_name = _('position')
        verbose_name_plural = _('positions')
        
    def __str__(self):
        return self.name
