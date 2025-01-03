from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from .base import BaseView


class Delete(BaseView):
    next = None
    action = ["delete"]
    template_name = "delete.html"
    
    def get(self, request, app, model):
        model = self.get_model()
        query = {k:v.split(',') if '__in' in k else v for k, v in request.GET.dict().items()}
        #if not query:
        #    raise Http404(_("Query is required for delete action"))
        qs = self.get_queryset().filter(**query)
        return render(request, self.template_name, locals())

    def post(self, request, app, model):
        model = self.get_model()
        query = {k:v.split(',') if '__in' in k else v for k, v in request.GET.dict().items()}
        if not query:
            raise Http404(_("Query is required for delete action"))
        qs = self.get_queryset().filter(**query)
        qs.delete()

        """
        # To-Do: To prevent delete of approved object by creator
        LogEntry.objects.log_action(**{
            'user_id': request.user.id,
            'content_type_id': ContentType.objects.get_for_model(model).id,
            'object_id': obj.pk,
            'object_repr': force_str(obj),
            'action_flag': DELETION
        })
        """

        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)