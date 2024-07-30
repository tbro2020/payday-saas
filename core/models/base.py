from django_currentuser.db.models import CurrentUserField
from django.utils.translation import gettext as _
from crispy_forms.layout import Layout
from django.urls import reverse_lazy

from .managers.base import CustomManager
from .fields import JSONField
from django.db import models

from api.serializers import model_serializer_factory

class Base(models.Model):
    updated_by = CurrentUserField(verbose_name=_('mis à jour par') , related_name='%(app_label)s_%(class)s_updated_by', on_update=True)
    created_by = CurrentUserField(verbose_name=_('créé par') , related_name='%(app_label)s_%(class)s_created_by')

    updated_at = models.DateTimeField(verbose_name=_('mis à jour le/à'), auto_now=True)
    created_at = models.DateTimeField(verbose_name=_('créé le/à'), auto_now_add=True)
    
    organization = models.ForeignKey(
        'core.organization', 
        verbose_name=_('organisation'), 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        default=None, 
        editable=False
    )

    metadata = JSONField(verbose_name=_('meta'), default=dict, blank=True)
    objects = CustomManager()

    list_display = ('id', 'name')
    search_fields = ()
    layout = Layout()
    list_filter = ()

    def __str__(self):
        return self.name
    
    @property
    def serialized(self):
        serializer = model_serializer_factory(self._meta.model)
        return serializer(self).data
    
    def get_absolute_url(self):
        return reverse_lazy('core:change', args=[self._meta.app_label, self._meta.model_name, self.pk])
    
    def delete_qs(request, qs):
        pass
    delete_qs.short_description = _('supprimer(s)')
    delete_qs.permissions = ['delete']

    actions = [] #[delete_qs]


    class Meta:
        abstract = True