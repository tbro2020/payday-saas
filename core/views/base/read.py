from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from crispy_forms.layout import Layout
from django.apps import apps

from core.forms import modelform_factory, InlineFormSetHelper
from django.urls import reverse_lazy
from django.contrib import messages
from .base import BaseView


class Read(BaseView):
    next = None
    action = ["view"]
    template_name = "read.html"
    inline_formset_helper = InlineFormSetHelper()

    def can_read(self, obj=None):
        user = self.request.user
        if user.is_superuser or user.is_staff: return True
        app, model = self.kwargs['app'], self.kwargs['model']
        model = apps.get_model(app, model_name=model)

        if not obj:
            obj = get_object_or_404(model, **{model._meta.pk.name: self.kwargs['pk']})
        
        approbations = list(self.approvers().values_list('user__email', flat=True))
        approbations.append(obj.created_by.email)

        return user.email in approbations

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)

        if not self.can_read():
            messages.warning(request, _('Vous n\'avez pas permission d\'effectuer cette action'))
            return redirect(reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        
        form = modelform_factory(model, fields=fields)
        form = form(instance=obj)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=True, extra=1) for inline in formsets]
        formsets = [formset(instance=obj) for formset in formsets]
        
        return render(request, self.template_name, locals())