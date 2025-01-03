from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib.admin.models import LogEntry
from django.forms.models import model_to_dict
from django.utils.encoding import force_str


class LoggerMixin:
    def logs(self):
        pk = self.kwargs.get('pk')
        content_type = self.get_content_type()
        return LogEntry.objects.filter(content_type=content_type, object_id=pk).values('change_message', 'action_time')
    
    def generate_change_message(self, old_instance, new_instance):
        fields = [field.name for field in new_instance._meta.fields]
        old_data = model_to_dict(old_instance, fields=fields)
        new_data = model_to_dict(new_instance, fields=fields)
        change_messages = [
            _(f"Field '{new_instance._meta.get_field(field).verbose_name}' changed from '{old_value}' to '{new_value}'.")
            for field in fields if (old_value := old_data.get(field)) != (new_value := new_data.get(field))
        ]
        return "; ".join(change_messages) if change_messages else None

    def log(self, model, form, action, change_message):
        if change_message:
            return LogEntry.objects.log_action(
                user_id=self.request.user.id,
                content_type_id=ContentType.objects.get_for_model(model).id,
                object_id=form.instance.pk,
                object_repr=force_str(str(form.instance)),
                action_flag=action,
                change_message=change_message
            )