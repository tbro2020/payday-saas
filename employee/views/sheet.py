from django.shortcuts import render, get_object_or_404
from core.forms import modelform_factory
from core.views import BaseView

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from employee.models import Employee
from django.apps import apps

class Sheet(BaseView):
    template_name = "employee/sheet.html"

    def get(self, request, pk):
        obj = get_object_or_404(Employee, pk=pk)
        fields = getattr(Employee, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()]

        form = modelform_factory(Employee, fields=fields)
        form = form(instance=obj)

        activities = LogEntry.objects.filter(**{
            'content_type_id': ContentType.objects.get_for_model(Employee).id, 
            'object_id': pk
        })

        payslips = apps.get_model('payroll.payslip').objects.filter(**{
            'employee__registration_number': obj.registration_number
        })
        return render(request, self.template_name, locals())
