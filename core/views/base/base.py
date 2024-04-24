from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views import View

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

from django.utils.encoding import force_str
from django.apps import apps

class BaseView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = None

    def get_permission_required(self):
        data = self.kwargs
        if 'app' not in data or 'model' not in data: return []
        return [f"{data.get('app')}.{i}_{data.get('model')}" for i in self.action]
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.warning(self.request, _('Vous n\'avez pas permission d\'effectuer cette action'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def activities(self):
        pk = self.kwargs.get('pk')
        app = self.kwargs.get('app')
        model = self.kwargs.get('model')
        model = apps.get_model(app, model_name=model)
        content_type = ContentType.objects.get_for_model(model)
        return LogEntry.objects.filter(**{'content_type_id': content_type.id, 'object_id': pk})
    
    def log(self, model, form, action, formsets=None):
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(model).id,
            object_id=form.instance.pk,
            object_repr=force_str(str(form.instance)),
            action_flag=action,
            change_message=''.join([])
        )