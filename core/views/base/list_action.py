from django.utils.translation import gettext as _
from django.apps import apps
from .base import BaseView

from django.shortcuts import redirect
from django.contrib import messages

class ListAction(BaseView):

    def get_action(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        model = apps.get_model(app, model_name=model)
        action = getattr(model, self.kwargs['action'])
        return getattr(action, 'permissions', [])

    def post(self, request, app, model, action):
        model = apps.get_model(app, model_name=model)

        qs = model.objects._all(
            subdomain=request.subdomain
        ).select_related().prefetch_related() if hasattr(model, '_all') else model.objects.all()
        qs = qs.none() # apply the fitler

        action = getattr(model, action)
        action(request, qs)
        
        return redirect(request.META.get('HTTP_REFERER'))