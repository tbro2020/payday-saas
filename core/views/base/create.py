from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib import messages

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION
from django.shortcuts import render, redirect
from crispy_forms.layout import Layout
from django.apps import apps
from .base import BaseView


class Create(BaseView):
    next = None
    action = ["add"]
    template_name = "create.html"
    inline_formset_helper = InlineFormSetHelper()
    
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        
        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields

        initial = {field:request.user.employee for field in fields if field == 'employee' and not request.user.is_superuser}
        form = modelform_factory(model, fields=fields)
        form = form(initial=initial)

        if not request.user.is_superuser and 'employee' in form.fields:
            form.fields['employee'].widget.attrs['disabled'] = 'disabled'
        
        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=False, extra=1) for inline in formsets]
        
        return render(request, self.template_name, locals())
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)

        fields = getattr(model, 'layout', '__all__')
        fields = [field.name for field in fields.get_field_names()] if isinstance(fields, Layout) else fields
        
        initial = {field:request.user.employee for field in fields if field == 'employee' and not request.user.is_superuser}
        form = modelform_factory(model, fields=fields)
        form = form(request.POST or None, request.FILES or None, initial=initial)

        if not request.user.is_superuser and 'employee' in form.fields:
            form.fields['employee'].widget.attrs['disabled'] = 'disabled'

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=getattr(inline, 'inline_form_fields', '__all__'), can_delete=False, extra=1) for inline in formsets]
        formsets = [formset(request.POST or None, request.FILES or None) for formset in formsets]

        if not form.is_valid() or False in [formset.is_valid() for formset in formsets]:
            [messages.error(request, str(error)) for error in form.errors]
            return render(request, self.template_name, locals())

        if hasattr(form.instance, 'organization'):
            form.instance.organization = request.organization
        form.save()


        for formset in formsets:
            qs = formset.save(commit=False)
            for obj in qs:
                setattr(obj, formset.fk.name, form.instance)
                obj.save()

        # Log
        self.log(model, form, action=ADDITION, formsets=formsets)
        
        messages.add_message(request, messages.SUCCESS, message=_('Le {model} a été créé avec succès').format(**{'model': model._meta.model_name}))
        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)