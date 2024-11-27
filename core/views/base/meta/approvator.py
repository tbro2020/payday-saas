from django.apps import apps

class Approvator:
    def is_approver(self):
        return self.approvers().filter(user=self.request.user).exists()

    def approvers(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        user_approver_model = apps.get_model('core', 'usercontenttypeapprover')
        return user_approver_model.objects.filter(
            content_type_approver__content_type__app_label=app,
            content_type_approver__content_type__model=model
        )
    
    def approvals(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        approval_model = apps.get_model('core', 'approval')
        return approval_model.objects.filter(
            content_type__app_label=app,
            content_type__model=model,
            object_pk=self.kwargs.get('pk', None)
        )

    def is_full_approved(self):
        return self.approvals().filter(action='approved').count() == self.approvers().count()

    def approbations(self):
        approvers = self.approvers().values_list('user__email', flat=True)
        approvals = self.approvals().values('created_by__email', 'action', 'comment')
        approval_dict = {approval['created_by__email']: {'action': approval['action'], 'comment': approval['comment']} for approval in approvals}
        unique_emails = set(list(approvers) + [approval['created_by__email'] for approval in approvals])
        return {email: approval_dict.get(email, {}) for email in unique_emails}