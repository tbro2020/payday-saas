from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .base import BaseView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from core.models import Widget

#@method_decorator(cache_page(60 * 15), name='dispatch')
class Home(BaseView):   
    template_name = "home.html"

    def get_employee(self):
        try:
            return self.request.user.employee
        except:
            return None

    def get(self, request):
        if not any([request.user.is_staff, request.user.is_superuser]):
            if employee:=self.get_employee():
                return redirect(employee.get_absolute_url())
            return redirect(reverse_lazy('core:password-change'))
        
        widgets = [{
            'title': widget.name,
            'content': widget.render(request),
            'column': widget.column,
        } for widget in Widget.objects.all()]
        return render(request, self.template_name, locals())