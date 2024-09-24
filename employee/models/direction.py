from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Direction(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)
    
    list_display = ('id', 'name')
    search_fields = ('name')
    layout = Layout('name')

    class Meta:
        verbose_name = _('departement')
        verbose_name_plural = _('departements')
        
    def __str__(self):
        return self.name
