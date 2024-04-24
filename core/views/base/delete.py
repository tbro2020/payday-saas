from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.apps import apps
from .base import BaseView


class Delete(BaseView):
    next = None
    action = ["delete"]
    template_name = "delete.html"
    
    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)
        return render(request, self.template_name, locals())

    def post(self, request, app, model, pk):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, id=pk)

        # To-Do: To prevent delete of approved object by creator
        LogEntry.objects.log_action(**{
            'user_id': request.user.id,
            'content_type_id': ContentType.objects.get_for_model(model).id,
            'object_id': obj.pk,
            'object_repr': force_str(obj),
            'action_flag': DELETION
        })

        obj.delete()
        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)