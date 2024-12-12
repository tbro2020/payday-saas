from crispy_forms.layout import Layout, Column, Row
from django.utils.translation import gettext as _

from core.models import fields
from .base import Base


class Preference(Base):
    key = fields.CharField(_('clé'), max_length=100, unique=True)
    value = fields.CharField(_('valeur'), max_length=100)
    
    search_fields = ('key', 'value')
    list_display = ('id', 'key', 'value')
    layout = Layout(Row(Column('key'), Column('value')))
    
    @property
    def name(self):
        return self.key
    
    @staticmethod
    def get(key, default=None):
        return Preference.objects.filter(key=key).first()

    class Meta:
        verbose_name = _('préférence')
        verbose_name_plural = _('préférences')