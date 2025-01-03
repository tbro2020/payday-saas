from django.utils.translation import gettext as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Layout, Column, Row, Fieldset
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import Base, fields

class Permission(Base):
    updated_by, created_by = None, None

    user = fields.ModelSelectField(
        'core.user',
        verbose_name=_("utilisateur"),
        related_name='permissions',
        inline=False
    )

    role = fields.ModelSelectField(
        'core.role',
        verbose_name=_("rôle"),
        related_name='permissions',
        inline=False
    )

    content_type = fields.ForeignKey(
        ContentType,
        verbose_name=_("type de contenu"),
        limit_choices_to={
            'app_label__in': ['core', 'employee', 'payroll']
        },
        related_name='permissions',
        inline=True
    )

    level = fields.IntegerField(
        verbose_name=_('niveau'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        inline=True
    )

    add = fields.BooleanField(
        verbose_name=_('ajouter'),
        default=False,
        inline=True
    )

    view = fields.BooleanField(
        verbose_name=_('voir'),
        default=False,
        inline=True
    )

    change = fields.BooleanField(
        verbose_name=_('change'),
        default=False,
        inline=True
    )

    delete = fields.BooleanField(
        verbose_name=_('supprime'),
        default=False,
        inline=True
    )

    export = fields.BooleanField(
        verbose_name=_('exportation'),
        default=False,
        inline=True
    )

    layout = Layout(
        Row(
            Column('user'),
            Column('content_type'),
        ),
        Fieldset(
            _('Permissions'),
            Row(
                Column('view'),
                Column('change'),
                Column('create'),
                Column('delete'),
                Column('export'),
            )
        ),
    )

    @property
    def name(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        unique_together = ("content_type", "user")