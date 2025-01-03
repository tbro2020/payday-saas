from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.db import models
from django.urls import reverse_lazy
from crispy_forms.bootstrap import FieldWithButtons, Field, StrictButton
from crispy_forms.layout import Layout, Row, Column
from core.models import fields, Base
from core.utils import upload_directory_file


class ImporterStatus(models.TextChoices):
    """Enumeration for Importer statuses."""
    PROCESSING = 'processing', _('en cours')
    PENDING = 'pending', _('en attente')
    SUCCESS = 'success', _('succès')
    ERROR = 'error', _('erreur')


class Importer(Base):
    """Model for managing file imports with associated content type and status."""
    status = fields.CharField(
        max_length=255,
        verbose_name=_('status'),
        choices=ImporterStatus.choices,
        default=ImporterStatus.PENDING,
    )

    content_type = fields.ForeignKey(
        ContentType,
        verbose_name=_('type de contenu'),
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'app_label__in': [
                'core',
            ],
            'model__in': [
                'preference',
                'widget'
            ],
        }
    )

    message = fields.TextField(
        verbose_name=_('message'),
        blank=True,
        null=True,
        default=None,
    )

    document = fields.ImporterField(
        upload_to=upload_directory_file,
        verbose_name=_('document'),
    )

    # Define the layout for Crispy Forms.
    layout = Layout(
        Row(
            Column(
                FieldWithButtons(
                    Field("content_type", css_class='col'),
                    StrictButton(
                        _('Télécharger le modèle'),
                        css_class='btn btn-light-info col',
                        onclick=(
                            "window.open('/canvas/download/' + "
                            "$('#id_content_type').val(), '_blank');"
                        ),
                    ),
                    css_class='col',
                ),
                css_class='col',
            ),
            Column('document'),
        )
    )

    list_display = ('id', 'content_type', 'status', 'message', 'updated_at')
    list_filter = ('status', 'content_type')

    def get_absolute_url(self):
        """Generate the absolute URL for this importer."""
        return reverse_lazy(
            'core:list',
            kwargs={
                'app': self.content_type.app_label,
                'model': self.content_type.model,
            },
        )

    @property
    def name(self):
        """Return the name of the uploaded document."""
        return self.document.name

    class Meta:
        verbose_name = _('importateur')
        verbose_name_plural = _('importateurs')