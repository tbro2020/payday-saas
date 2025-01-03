from crispy_forms.layout import Layout, Column, Fieldset, Row as CrispyRow
from django.utils.translation import gettext as _
from core.models import Base, fields

class RowLevelSecurity(Base):
    updated_by, created_by = None, None

    user = fields.ModelSelectField(
        'core.user',
        verbose_name=_("utilisateur"),
        related_name='rows',
        inline=False
    )

    role = fields.ModelSelectField(
        'core.role',
        verbose_name=_("rôle"),
        related_name='rows',
        inline=False
    )

    content_type = fields.ForeignKey(
        'contenttypes.contenttype',
        verbose_name=_("type de contenu"),
        limit_choices_to={
            'app_label__in': ['core', 'employee', 'payroll']
        },
        related_name='rows',
        inline=True
    )

    field = fields.CharField(
        verbose_name=_("champ"),
        max_length=255,
        inline=True,
        level=1
    )

    value = fields.CharField(
        verbose_name=_("valeur"),
        max_length=255,
        inline=True
    )

    layout = Layout(
        CrispyRow(
            Column('user'),
            Column('content_type'),
        ),
        Fieldset(
            _('Row'),
            CrispyRow(
                Column('field'),
                Column('value'),
            )
        ),
    )

    def name(self):
        return f"{self.user} - {self.content_type}"

    class Meta:
        unique_together = ("content_type", "user", "field")
        verbose_name = _("sécurité au niveau de la ligne")
        verbose_name_plural = _("sécurités au niveau de la ligne")
