from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models


class Position(Base):
    name = models.CharField(verbose_name=_('nom'), max_length=100)
    working_days_per_month = models.IntegerField(verbose_name=_('jours de travail par mois'), default=30)

    layout = Layout('name', 'working_days_per_month')
    list_display = ('id', 'name', 'working_days_per_month')

    class Meta:
        verbose_name = _('poste')
        verbose_name_plural = _('postes')
        
    def __str__(self):
        return self.name
