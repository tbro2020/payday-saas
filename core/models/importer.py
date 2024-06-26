from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.db import models

from core.utils import upload_directory_file
from core.models.fields import ModelSelect
from core.models import Base

from crispy_forms.bootstrap import FieldWithButtons, Field, StrictButton
from crispy_forms.layout import Layout, Row, Column
from django.urls import reverse_lazy


class ImporterStatus(models.TextChoices):
    PROCESSING = 'processing', _('en cours')
    PENDING = 'pending', _('en attente')
    SUCCESS = 'success', _('succès')
    ERROR = 'error', _('erreur')


class Importer(Base):
    status = models.CharField(max_length=255, verbose_name=_('status'), choices=ImporterStatus.choices, default=ImporterStatus.PENDING)
    content_type = ModelSelect(ContentType, verbose_name=_('type de contenue'), null=True, on_delete=models.SET_NULL)
    message = models.TextField(verbose_name=_('message'), blank=True, null=True, default=None)
    document = models.FileField(upload_to=upload_directory_file, verbose_name=_('document'))

    layout = Layout(
        Row(
            Column(
                FieldWithButtons(
                    Field("content_type"), 
                    StrictButton(
                        'Télécharger le modèle', 
                        css_class='btn btn-light-info', 
                        onclick="window.open('/canvas/download/'+$('#id_content_type').val(), '_blank');"
                    )
                )
            ),
            Column('document')
        )
    )
    list_display = ('id', 'content_type', 'status', 'message', 'updated_at')

    def get_absolute_url(self):
        return reverse_lazy('core:list', kwargs={'app': self.content_type.app_label, 'model': self.content_type.model})

    @property
    def name(self):
        return self.document.name

    class Meta:
        verbose_name = _('importateur')
        verbose_name_plural = _('importateurs')