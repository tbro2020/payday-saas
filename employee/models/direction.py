from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields

class Direction(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)
    
    list_display = ('id', 'name')
    search_fields = ('name')
    layout = Layout('name')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('direction')
        verbose_name_plural = _('directions')
        
    def __str__(self):
        return self.name
