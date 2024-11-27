from django.utils.translation import gettext as _
from django.contrib.admin.models import LogEntry
from django.shortcuts import render
from .base import List

class ActivityLog(List):
    
    def get_list_display(self, model):
        list_display = ['action_time', 'content_type', 'object_id', 'change_message', 'user']
        list_display_order = {field: i for i, field in enumerate(list_display)}
        return sorted([field for field in model._meta.fields if field.name in list_display], key=lambda field: list_display_order[field.name])
    
    def get_list_filter(self, model):
        return ['content_type', 'action_flag', 'action_time']

    def get(self, request):
        self.kwargs['app'] = LogEntry._meta.app_label
        self.kwargs['model'] = LogEntry._meta.model_name
        return super().get(request, LogEntry._meta.app_label, LogEntry._meta.model_name)