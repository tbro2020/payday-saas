from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from crispy_forms.layout import Layout
from django.contrib import messages

from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views import View
from django.apps import apps
from .meta import *

class BaseView(LoginRequiredMixin, PermissionRequiredMixin, Approvator, Fielder, Logger, Documentor, View):
    template_name = None
    action = []

    def get_action(self):
        return self.action

    def get_permission_required(self):
        if not self.request.user.is_authenticated:
            return []
        app, model = self.kwargs.get('app'), self.kwargs.get('model')
        if app and model:
            return [f"{app}.{act}_{model}" for act in self.get_action()]
        return []
    
    def handle_no_permission(self):
        if self.get_permission_required():
            messages.warning(self.request, _("You don't have permission to perform this action."))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy('login')))
    
    def get_content_type(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        return ContentType.objects.get(app_label=app, model=model)