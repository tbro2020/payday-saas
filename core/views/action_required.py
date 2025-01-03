# from core.models import UserContentTypeApprover, Approval
from django.shortcuts import render
from django.apps import apps
from .base import BaseView

class ActionRequired(BaseView):
    template_name = 'required.html'

    def get(self, request):
        """
        fields = [f'content_type_approver__content_type__{field}' for field in ['app_label', 'model']]
        approvers = UserContentTypeApprover.objects.filter(user=request.user)
        approvers = approvers.values(*fields).distinct()

        # search for all objects that are not approved
        qs = []
        for approver in approvers:
            app, model_name = approver.values()
            model = apps.get_model(app_label=app, model_name=model_name)
            ids = list(map(str, model.objects.values_list('id', flat=True)))

            # remove ids that have already been approved
            approvals = Approval.objects.filter(**{
                'content_type__model': model_name,
                'content_type__app_label': app,
                'created_by': request.user,
                'object_pk__in': ids,
            }).values_list('object_pk', flat=True)
            qs += [{
                'created_at': obj.created_at,
                'created_by': obj.created_by,

                'pk': obj.pk,
                'app': model._meta.app_label,
                'model': model._meta.model_name,
                'model_verbose': model._meta.verbose_name,
                'description': f'{obj.created_by} is requesting your approval',
            } for obj in model.objects.filter(id__in=list(set(ids) - set(list(approvals))))]
        """
        return render(request, self.template_name, locals())