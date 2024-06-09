from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models.fields import DateField
from django.db import models

from core.models import Base


class Holiday(Base):
    paid = models.BooleanField(_('payé'), default=True)
    name = models.CharField(_('nom'), max_length=100)
    start_dt = DateField(_('du'))
    end_dt = DateField(_('au'))
    

    layout = Layout('name', Row(Column('start_dt', css_class='col-md-6 col-sm-12'), Column('end_dt', css_class='col-md-6 col-sm-12')), 'paid')
    list_display = ('id', 'name', 'start_dt', 'end_dt')
    search_fields = ('name',)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Fériée')
        verbose_name_plural = _('Fériées')
