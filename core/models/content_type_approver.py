from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from crispy_forms.layout import Layout

from core.models import fields
from core.models import Base
from django.db import models

class ContentTypeApprover(Base):
    content_type = fields.ModelSelectField(ContentType, verbose_name=_('type de contenu'), on_delete=models.CASCADE)
    
    search_field = ('content_type__model',)
    list_display = ('id', 'content_type',)
    
    inlines = ['core.usercontenttypeapprover',]
    layout = Layout('content_type',)

    @property
    def name(self):
        return self.content_type.name

    class Meta:
        verbose_name = _('approbation')
        verbose_name_plural = _('approbations')

class UserContentTypeApprover(Base):
    content_type_approver = fields.ModelSelectField(ContentTypeApprover, verbose_name=_('type de contenu'), on_delete=models.CASCADE, inline=True)
    user = fields.ModelSelectField(get_user_model(), verbose_name=_('utilisateur'), on_delete=models.CASCADE, inline=True)
    
    search_field = ('user__email', 'content_type_approver__content_type__model')
    list_display = ('id', 'user', 'content_type_approver', 'updated_at')
    inline_form_fields = ('user', 'content_type_approver')
    layout = Layout('user', 'content_type_approver')

    @property
    def name(self):
        return f"{self.content_type_approver.content_type.name}/{self.user.name}"
    
    class Meta:
        verbose_name = _('approbateur')
        verbose_name_plural = _('approbateurs')
