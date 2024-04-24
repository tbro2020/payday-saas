from django.utils.translation import gettext as _
from core.models.fields import AceField
from crispy_forms.layout import Layout
from core.models import Base
from django.db import models

class JobFrequencyChoice(models.TextChoices):
    APPROVED = "DAILY", _("quotidien")

class Job(Base):
    name = models.CharField(max_length=255, verbose_name=_('Nom'))
    job = AceField(mode='python', verbose_name=_('job'), default='0')
    frequency = models.CharField(max_length=10, choices=JobFrequencyChoice.choices, verbose_name=_('Fréquence'))

    layout = Layout('name', 'frequency', 'job')
    list_display = ('id', 'name', 'frequency')
    list_filter = ('frequency',)
    search_fields = ('name',)

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')