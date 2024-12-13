from django.utils.translation import gettext as _
from django.shortcuts import render
from core.views import BaseView
from django.http import Http404
from django.apps import apps



class Slips(BaseView):
    template_name = "payroll/slip.html"

    def get(self, request):
        app, model = 'payroll', 'payslip'
        self.kwargs['model'] = model
        self.kwargs['app'] = app

        model = apps.get_model(app, model)
        qs = model.objects.filter(**request.GET.dict())

        if not qs:
            raise Http404(_("No payslips found"))

        return render(request, self.template_name, locals())