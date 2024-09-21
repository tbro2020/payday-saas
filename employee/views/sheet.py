from django.shortcuts import render, get_object_or_404
from core.views import BaseView

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from employee.models import Employee
from django.apps import apps

class Sheet(BaseView):
    template_name = "employee/sheet.html"

    def get(self, request, pk):
        obj = get_object_or_404(Employee, pk=pk)
        logs = LogEntry.objects.filter(**{
            'content_type_id': ContentType.objects.get_for_model(Employee).id, 
            'object_id': pk
        }).values('action_time', 'change_message')
        return render(request, self.template_name, locals())
