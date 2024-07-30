from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.db.models import Count
from employee.models import *

#@method_decorator(cache_page(60 * 15), name='dispatch')
class Home(BaseView):   
    template_name = "home.html"

    def get(self, request):
        employees = Employee.objects.all().select_related().prefetch_related()
        employees_by_statues = employees.values('status__name').annotate(count=Count('status__name'))
        employees_by_statues = employees_by_statues.filter(count__gt=0)
        employees_by_statues = list(employees_by_statues)

        return render(request, self.template_name, locals())