from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from django.db import models

from core.models import Base, fields
from .direction import Direction

class SubDirection(Base):
    direction = fields.ModelSelectField(Direction, verbose_name=_('direction'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    search_fields = ('direction__name', 'name')
    list_display = ('id', 'direction', 'name')
    list_filter = ('direction',)
    
    layout = Layout('direction', 'name')
    inline_form_fields = ('name',)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('sous-direction')
        verbose_name_plural = _('sous-directions')
        
    def __str__(self):
        return self.name
