from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from core.views import BaseView
from django.apps import apps

class Notification(BaseView):
    action = ['view']

    def get(self, request, pk):
        model = apps.get_model('core', 'notification')
        obj = get_object_or_404(model, pk=pk)
        obj.view()
        
        return redirect(obj.redirect or reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'notification'}))