from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView

from core.models import Widget
from datetime import date



class Home(BaseView):
    today = date.today()

    def get(self, request):
        permissions = [permission.split('.')[-1] for permission in request.user.get_all_permissions()]
        widgets = Widget.objects.filter(permissions__codename__in=permissions).distinct().order_by('id')
        
        from django.db.models import Count
        from django.apps import apps
        from datetime import date

        attendances = apps.get_model('employee', 'attendance')
        attendances = attendances.objects.filter(date__year=date.today().year)
        attendances = attendances.filter(direction='OUT').values('employee', 'date')
        attendances = list(attendances.values('date').annotate(count=Count('employee')))
        print(attendances)
        
        return render(request, "home.html", locals())