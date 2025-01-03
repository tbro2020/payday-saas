from django.utils.translation import gettext as _
from crispy_forms.layout import Layout

from core.models import Base, fields

class Role(Base):
    name = fields.CharField(
        verbose_name=_("nom"),
        max_length=255,
        unique=True
    )

    inlines = ('core.permission', 'core.rowlevelsecurity',)
    list_display = ('id', 'name')
    layout = Layout('name')

    class Meta:
        verbose_name = _("rôle")
        verbose_name_plural = _("rôles")