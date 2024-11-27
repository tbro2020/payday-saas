from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields

class Grade(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name', 'metadata')
    search_fields = ('name')
    list_display = ('id', 'name')

    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')
        
    def __str__(self):
        return self.name
