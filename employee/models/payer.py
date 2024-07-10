from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _

from core.models import Base
from django.db import models


class Payer(Base):
    category = models.CharField(verbose_name=_('catégorie'), max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name=_('nom'), max_length=100)

    layout = Layout(Row(Column('category'),Column('name')), 'metadata')
    list_display = ('id', 'category', 'name')
    search_fields = ('name')

    def __str__(self) -> str:
        if not self.category:
            return self.name
        return "{}/{}".format(self.category, self.name)

    class Meta:
        verbose_name = _('banque')
        verbose_name_plural = _('banques')
        
    def __str__(self):
        return self.name
