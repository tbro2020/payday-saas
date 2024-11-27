from django.contrib.contenttypes.models import ContentType
from django_currentuser.db.models import CurrentUserField
from django.utils.translation import gettext as _
from .managers.base import CustomManager
from crispy_forms.layout import Layout
from django.urls import reverse_lazy

from core.models import fields
from django.db import models

from api.serializers import model_serializer_factory
from django.apps import apps

class Base(models.Model):
    updated_by = CurrentUserField(verbose_name=_('mis à jour par') , related_name='%(app_label)s_%(class)s_updated_by', on_update=True)
    created_by = CurrentUserField(verbose_name=_('créé par') , related_name='%(app_label)s_%(class)s_created_by')

    approved = fields.BooleanField(verbose_name=_('approuvé'), default=False, editable=False)
    updated_at = fields.DateTimeField(verbose_name=_('mis à jour le/à'), auto_now=True)
    created_at = fields.DateTimeField(verbose_name=_('créé le/à'), auto_now_add=True)
    
    organization = fields.ForeignKey(
        'core.organization', 
        verbose_name=_('organisation'), 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        default=None, 
        editable=False
    )

    metadata = fields.JSONField(verbose_name=_('meta'), default=dict, blank=True)
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

    def approvers(self):
        app, model = self._meta.app_label, self._meta.model_name
        user_content_type_approver = apps.get_model('core', 'usercontenttypeapprover')
        return user_content_type_approver.objects.filter(**{
            'content_type_approver__content_type__app_label': app,
            'content_type_approver__content_type__model': model
        })
    
    def approvals(self):
        app, model = self._meta.app_label, self._meta.model_name
        approval = apps.get_model('core', 'approval')
        return approval.objects.filter(**{
            'content_type__app_label': app,
            'content_type__model': model,
            'object_pk': self.pk
        })

    def approve(self):
        content_type = ContentType.objects.get_for_model(self)

        UserContentTypeApprover = apps.get_model('core', 'usercontenttypeapprover')
        approvers = UserContentTypeApprover.objects.filter(**{
            'content_type_approver__content_type': content_type
        }).values('user').distinct()

        Approval = apps.get_model('core', 'approval')
        approvals = Approval.objects.filter(**{
            'content_type': content_type,
            'object_pk': self.pk,
            'action': 'approve'
        }).values('content_type', 'object_pk', 'action').distinct()

        self.approved = False
        if approvers.count() == approvals.count():
            self.approved = True
            self.send_notification()
        self.save()

    def send_notification(self):
        model = apps.get_model('core', 'notification')
        model.objects.create(
            _from=self.updated_by,
            _to=self.created_by,
            redirect=self.get_absolute_url(),
            subject=_('Approbation #{model}').format(model=self._meta.verbose_name),
            message=_('Demande #{} a été approuvée'.format(self.pk))
        )

    actions = [] #[delete_qs]

    class Meta:
        abstract = True