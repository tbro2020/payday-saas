from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Grade(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name', 'metadata')
    list_display = ('id', 'name')
    search_fields = ('name')

    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')
        
    def __str__(self):
        return self.name
