from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext as _
from core.models import Base, fields


class Holiday(Base):
    name = fields.CharField(_('nom'), max_length=100)
    start_dt = fields.DateField(_('du'))
    end_dt = fields.DateField(_('au'))

    layout = Layout('name', Row(Column('start_dt'), Column('end_dt')))
    list_display = ('id', 'name', 'start_dt', 'end_dt')
    search_fields = ('name',)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Fériée')
        verbose_name_plural = _('Fériées')
