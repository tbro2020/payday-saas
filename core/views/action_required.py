from django.shortcuts import render
from .base import BaseView

class ActionRequired(BaseView):
    template_name = 'action_required.html'

    def get(self, request):
        return render(request, self.template_name, locals())