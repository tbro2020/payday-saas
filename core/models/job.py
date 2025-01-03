from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _

from core.models import Base, fields
from django.db import models

class JobFrequencyChoice(models.TextChoices):
    HOURLY = "HOURLY", _("horaire")
    DAILY = "DAILY", _("quotidien")
    WEEKLY = "WEEKLY", _("hebdomadaire")
    MONTHLY = "MONTHLY", _("mensuel")
    YEARLY = "YEARLY", _("annuel")

class Job(Base):
    frequency = fields.CharField(
        max_length=10, 
        choices=JobFrequencyChoice.choices, 
        verbose_name=_('fréquence')
    )
    job = fields.AceField(
        mode='python', 
        verbose_name=_('job'), 
        default='0'
    )
    name = fields.CharField(
        max_length=255, 
        verbose_name=_('nom')
    )

    is_active = fields.BooleanField(
        default=True, 
        verbose_name=_('actif')
    )

    layout = Layout(
        Row(
            Column('name'),
            Column('frequency'),
        ), 
        'job'
    )
    list_display = ('id', 'name', 'frequency')
    list_filter = ('frequency',)
    search_fields = ('name',)

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')