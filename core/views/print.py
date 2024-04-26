from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import gettext as _
from django.contrib import messages

from django.template import Context, Template
from core.views import BaseView
from django.apps import apps

class Print(BaseView):
    action = ["view"]
    template_name = 'print.html'

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, id=pk)

        if not obj.template:
            messages.warning(request, _('Impossible de trouver le modèle du document'))
            return redirect(request.META.get('HTTP_REFERER'))

        template = Template(obj.template.content)
        context = Context(vars(obj))
        context['obj'] = obj

        template = template.render(context)
        return render(request, self.template_name, locals())
