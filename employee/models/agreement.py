from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base, fields



class Agreement(Base):
    name = fields.CharField(verbose_name=_('nom'), max_length=100, unique=True)

    layout = Layout('name')
    search_fields = ('name') 
    list_display = ('id', 'name')

    class Meta:
        verbose_name = _('contrat')
        verbose_name_plural = _('contrats')
