from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import gettext as _
from django.contrib import messages

from django.template import Context, Template
from core.views import BaseView
from django.apps import apps

class Print(BaseView):
    action = ["view"]
    template_name = 'print.html'

    def get(self, request, document, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **{
            model._meta.pk.name: pk
        })

        template = apps.get_model('core', 'template')
        template = template.objects.filter(id=document).first()

        if not template:
            messages.warning(request, _('Impossible de trouver le modèle du document'))
            return redirect(request.META.get('HTTP_REFERER'))

        template = Template(template.content).render(Context(locals()))
        return render(request, self.template_name, locals())
