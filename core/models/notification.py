from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from crispy_forms.layout import Layout

from core.models import Base, fields

class Notification(Base):
    _from = fields.ModelSelectField(
        get_user_model(), 
        verbose_name=_('de'), 
        related_name='sent_notifications', 
        on_delete=models.CASCADE
    )
    _to = fields.ModelSelectField(
        get_user_model(), 
        verbose_name=_('à'), 
        related_name='notifications', 
        on_delete=models.CASCADE
    )

    redirect = fields.CharField(
        verbose_name=_('rediriger vers'), 
        max_length=255, 
        blank=True, 
        null=True
    )
    subject = fields.CharField(
        verbose_name=_('sujet'), 
        max_length=255
    )
    viewed = fields.BooleanField(
        verbose_name=_('vu'), 
        default=False
    )
    message = fields.TextField(
        verbose_name=_('message')
    )

    list_display = ('viewed', 'subject', '_from', 'message', 'updated_at')
    layout = Layout('subject', 'message', '_from', '_to')
    search_fields = ('subject', 'message')
    list_filter = ('viewed',)

    @property
    def name(self):
        return self.subject

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('core:notification', args=[self.pk])
    
    def view(self):
        if self.viewed:
            return
        self.viewed = True
        self.save()

    class Meta:
        verbose_name_plural = _('notifications')
        verbose_name = _('notification')
        ordering = ['-created_at']
