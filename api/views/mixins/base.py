from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from core.mixins import FielderMixin, LoggerMixin
from django.views import View
from django.apps import apps

class BaseApiMixin:
    def get_content_type(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        return ContentType.objects.get(app_label=app, model=model)
    
    def get_model(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        return apps.get_model(app, model_name=model)
    
    def get_queryset(self):
        model = self.get_model()
        rls = self.request.user.get_user_rls(
            app=model._meta.app_label,
            model=model._meta.model_name
        )
        return model.objects.filter(**rls)