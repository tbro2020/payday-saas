from django.utils.translation import gettext as _
from core.models.base import Base, fields
from crispy_forms.layout import Layout

class TypeOfSanction(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100)

    class Meta:
        verbose_name = _('type de sanction')
        verbose_name_plural = _('types de sanction')

    search_fields = ('name',)
    list_display = ('id', 'name')
    layout = Layout('name', 'metadata')
