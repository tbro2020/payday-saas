from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields

class Designation(Base):
    working_days_per_month = fields.IntegerField(verbose_name=_('jours ouvrables par mois'), default=23)
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name', 'working_days_per_month')
    search_fields = ('name')
    list_display = ('id', 'name')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('position')
        verbose_name_plural = _('positions')
        
    def __str__(self):
        return self.name
