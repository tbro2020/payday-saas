from django.shortcuts import redirect, get_list_or_404, get_object_or_404, render
from django.utils.translation import gettext as _
from django.contrib import messages

from django.template import Context, Template
from core.views import BaseView
from django.apps import apps

from core import models

class Print(BaseView):
    action = ["view"]
    template_name = 'print.html'

    def get(self, request, document, app, model):
        query = {k: v.split(',') if '__in' in k else v for k, v in request.GET.items()}
        if not query:
            messages.warning(request, _('Impossible de trouver le modèle d\'object'))
            return redirect(request.META.get('HTTP_REFERER'))
        
        model = apps.get_model(app, model_name=model)
        qs = get_list_or_404(model, **query)

        template = get_object_or_404(models.Template, pk=document)
        if not template:
            messages.warning(request, _('Impossible de trouver le modèle du document'))
            return redirect(request.META.get('HTTP_REFERER'))

        # expensive operation [need to be review in the future]
        templates = [Template(template.content).render(Context(locals())) for obj in qs]
        return render(request, self.template_name, locals())
