from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields

class Branch(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name')
    search_fields = ('name') 
    list_display = ('id', 'name')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('site')
        verbose_name_plural = _('sites')
        
    def __str__(self):
        return self.name