from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Payer(Base):
    code = models.CharField(verbose_name=_('code'), null=True, default=None, max_length=10)
    name = models.CharField(verbose_name=_('nom'), max_length=100)

    list_display = ('id', 'code', 'name')
    layout = Layout('code', 'name', 'metadata')
    search_fields = ('name')

    class Meta:
        verbose_name = _('banque')
        verbose_name_plural = _('banques')
        
    def __str__(self):
        return self.name
