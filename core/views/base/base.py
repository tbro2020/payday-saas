from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views import View

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.forms.models import model_to_dict

from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.apps import apps



class BaseView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = None
    action = []

    def get_action(self):
        return self.action

    def get_permission_required(self):
        if not self.request.user.is_authenticated: return []
        if 'app' not in self.kwargs or 'model' not in self.kwargs: return []
        return [f"{self.kwargs.get('app')}.{i}_{self.kwargs.get('model')}" for i in self.get_action()]
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.get_permission_required():
            messages.warning(self.request, _('Vous n\'avez pas permission d\'effectuer cette action'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy('login')))

    def activities(self):
        pk = self.kwargs.get('pk')
        app = self.kwargs.get('app')
        model = self.kwargs.get('model')
        model = apps.get_model(app, model_name=model)
        content_type = ContentType.objects.get_for_model(model)
        return LogEntry.objects.filter(**{'content_type_id': content_type.id, 'object_id': pk})
    
    def generate_change_message(self, old_instance, new_instance):
        """
        Compares the field values of two model instances and generates a change message.
        
        :param old_instance: The original model instance (before changes).
        :param new_instance: The modified model instance (after changes).
        :return: A change message string describing the fields that have changed.
        """
        # Get the field names of the model
        fields = [field.name for field in new_instance._meta.fields]

        # Get the old and new data as dictionaries
        old_data = model_to_dict(old_instance, fields=fields)
        new_data = model_to_dict(new_instance, fields=fields)

        # List to hold change messages
        change_messages = []

        # Compare the old and new data
        for field in fields:
            old_value = old_data.get(field)
            new_value = new_data.get(field)

            # If the field value has changed, append a message
            if old_value != new_value:
                change_messages.append(
                    _(f"Field '{field}' changed from '{old_value}' to '{new_value}'.")
                )

        # Join all change messages into a single string
        if change_messages:
            return "; ".join(change_messages)
        else:
            return _("No changes made.")

    def log(self, model, form, action, change_message=''):
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(model).id,
            object_id=form.instance.pk,
            object_repr=force_str(str(form.instance)),
            action_flag=action,
            change_message=change_message
        )