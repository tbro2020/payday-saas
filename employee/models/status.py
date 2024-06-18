from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Status(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    search_fields = ('name')
    list_display = ('id', 'name')
    layout = Layout('name', 'metadata')

    class Meta:
        verbose_name = _('code activité')
        verbose_name_plural = _('code activités')
        
    def __str__(self):
        return self.name
