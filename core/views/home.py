from django.utils.translation import gettext as _
from django.shortcuts import render
from .base import BaseView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from core.models import Widget

#@method_decorator(cache_page(60 * 15), name='dispatch')
class Home(BaseView):   
    template_name = "home.html"

    def get(self, request):
        widgets = [{
            'title': widget.name,
            'content': widget.render(request),
            'column': widget.column,
        } for widget in Widget.objects.filter(active=True) if widget.has_permission(request.user)]
        return render(request, self.template_name, locals())