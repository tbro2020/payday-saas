from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from crispy_forms.layout import Layout
from django.urls import reverse_lazy
from django.contrib import messages
from django.apps import apps

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.admin.models import CHANGE
from .base import BaseView


class Change(BaseView):
    next = None
    action = ["change"]
    template_name = "change.html"
    inline_formset_helper = InlineFormSetHelper()

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)
        
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        
        form = modelform_factory(model, fields=fields)
        form = form(instance=obj)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=True, extra=1) for inline in formsets]
        formsets = [formset(instance=obj) for formset in formsets]
        
        return render(request, self.template_name, locals())

    def post(self, request, app, model, pk):
        model = apps.get_model(app, model)
        obj = get_object_or_404(model, pk=pk)
                
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        
        form = modelform_factory(model, fields=fields)
        form = form(request.POST or None, request.FILES or None, instance=obj)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=True, extra=1) for inline in formsets]
        formsets = [formset(request.POST or None, request.FILES or None, instance=obj) for formset in formsets]

        if not form.is_valid() or False in [formset.is_valid() for formset in formsets]:
            for error in form.errors: messages.error(request, str(error))
            return render(request, self.template_name, locals())

        form.save()
        [formset.save() for formset in formsets]

        self.log(model, form, action=CHANGE, formsets=formsets)
        messages.add_message(request, messages.SUCCESS,  message=_('Le {model} #{pk} a été mis à jour avec succès').format(**{'model': model._meta.model_name, 'pk': pk}))

        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)