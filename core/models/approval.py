from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout, Fieldset
from core.models import fields
from core.models import Base
from django.db import models

class ApprovalAction(models.TextChoices):
    APPROVE = 'approve', _('approuver')
    REJECT = 'reject', _('rejeter')

class Approval(Base):
    content_type = fields.ModelSelectField(ContentType, verbose_name=_('type de contenu'), null=True, on_delete=models.SET_NULL, editable=1)
    object_pk = fields.CharField(max_length=255, verbose_name=_('clé primaire de l\'objet'), editable=1)

    action = fields.CharField(max_length=10, choices=ApprovalAction.choices, verbose_name=_('action'))
    comment = fields.TextField(verbose_name=_('commentaire'), blank=True, null=True)

    list_display = ('id', 'content_type', 'object_pk', 'action', 'comment')
    search_field = ('content_type__model', 'object_pk')
    layout = Layout(
        Fieldset(
            _('Informations'),
            'content_type',
            'object_pk',
            css_class='bg-light p-3 mb-3 rounded'
        ),
        'action', 
        'comment'
    )

    @property
    def name(self):
        return f"{self.action} {self.content_type.name} {self.object_pk}"
    
    @property
    def object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_pk)
    
    class Meta:
        verbose_name = _('approbation')
        verbose_name_plural = _('approbations')