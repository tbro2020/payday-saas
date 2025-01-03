from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from core.mixins import FielderMixin, LoggerMixin
from django.views import View
from django.apps import apps

from django.conf import settings

class BaseView(LoginRequiredMixin, PermissionRequiredMixin, FielderMixin, LoggerMixin, View):
    actions = []
    template_name = None
    DEBUG = settings.DEBUG

    def get_actions(self):
        return self.actions
    
    def get_action_buttons(self):
        return []
    
    def get_template_name(self):
        return getattr(self.get_model(), 'list_template', self.template_name)
    
    def get_queryset(self):
        model = self.get_model()
        rls = self.request.user.get_user_rls(
            app=model._meta.app_label,
            model=model._meta.model_name
        )
        return model.objects.filter(**rls)

    def get_permission_required(self):
        if not self.request.user.is_authenticated: return []
        app, model = self.kwargs.get('app'), self.kwargs.get('model')
        return [f"{app}.{action}_{model}" for action in self.get_actions()]
        
    def handle_no_permission(self):
        if self.get_permission_required():
            messages.warning(self.request, _("You don't have permission to perform this action."))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy('login')))
    
    def get_content_type(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        return ContentType.objects.get(app_label=app, model=model)
    
    def get_model(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        return apps.get_model(app, model_name=model)
    
    def keywords(self):
        _keywords = [
            {'name': _('vrai'), 'meta': 'boolean', 'value': 'True'},
            {'name': _('faux'), 'meta': 'boolean', 'value': 'False'},
            {'name': _('null'), 'meta': 'null', 'value': 'None'},
            {'name': _('vide'), 'meta': 'empty', 'value': ''},
            {'name': _('aujourdhui'), 'meta': 'date', 'value': 'datetime.date.today()'},
            {'name': _('maintenant'), 'meta': 'datetime', 'value': 'datetime.datetime.now()'}
        ]
        models = [
            #apps.get_model('employee.employee'),
            #apps.get_model('payroll.payroll'),
            #apps.get_model('payroll.payslip'),
        ]
        exclude_fields = ['created_by', 'updated_by', 'updated_at', 'created_at']
        for model in models:
            for field in model._meta.fields:
                if field.name in exclude_fields:
                    continue
                if not field.is_relation:
                    _keywords.append({
                        'name': f'{model._meta.model_name}.{field.verbose_name.lower()}',
                        'meta': model._meta.verbose_name.lower(),
                        'value': f'{model._meta.model_name}.{field.name}'
                    })
                    continue
                if not field.related_model:
                    continue
                related_model = field.related_model
                for related_field in related_model._meta.fields:
                    if related_field.name in exclude_fields:
                        continue
                    _keywords.append({
                        'name': f'{related_field.verbose_name.lower()}',
                        'meta': related_model._meta.verbose_name.lower(),
                        'value': f"{model._meta.model_name}.{field.name}.{related_field.name}"
                    })
        return _keywords