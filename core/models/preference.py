from crispy_forms.layout import Layout, Column, Row
from django.utils.translation import gettext as _
from django.db import models
from .base import Base


class Preference(Base):
    key = models.CharField(_('clé'), max_length=100, unique=True)
    value = models.CharField(_('valeur'), max_length=100)
    
    search_fields = ('key', 'value')
    list_display = ('id', 'key', 'value')
    layout = Layout(Row(Column('key'), Column('value')), 'metadata')
    
    @property
    def name(self):
        return self.key
    
    @staticmethod
    def get(key):
        return Preference.objects.filter(key=key).first()

    class Meta:
        verbose_name = _('préférence')
        verbose_name_plural = _('préférences')