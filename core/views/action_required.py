from django.shortcuts import render
from .base import BaseView

class ActionRequired(BaseView):
    template_name = 'required.html'

    def get(self, request):
        return render(request, self.template_name, locals())