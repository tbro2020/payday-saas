from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields

class Grade(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name', '_metadata')
    list_display = ('id', 'name')
    search_fields = ('name')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')
        
    def __str__(self):
        return self.name
