from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Branch(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name')
    search_fields = ('name') 
    list_display = ('id', 'name')

    class Meta:
        verbose_name = _('zone')
        verbose_name_plural = _('zones')
        
    def __str__(self):
        return self.name