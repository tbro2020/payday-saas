from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib import messages

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.admin.models import ADDITION
from django.shortcuts import render, redirect
from django.apps import apps
from .base import BaseView


class Create(BaseView):
    next = None
    action = ["add"]
    template_name = "create.html"
    inline_formset_helper = InlineFormSetHelper()
    
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        fields = self.get_form_fields(model)

        initial = {field:request.user.employee for field in fields if field == 'employee' and not request.user.is_superuser}
        initial.update(request.GET.dict())

        form = modelform_factory(model, fields=fields)
        form = form(initial=initial)

        if not request.user.is_superuser and 'employee' in form.fields:
            form.fields['employee'].widget.attrs['disabled'] = 'disabled'
        
        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=self.get_inline_form_fields(inline), exclude=('metadata', 'created_by', 'updated_by'), can_delete=True, extra=1) for inline in formsets]
        formsets = [formset(queryset=formset.model.objects.none()) for formset in formsets]
        
        return render(request, self.template_name, locals())
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        fields = self.get_form_fields(model)
        
        initial = {field:request.user.employee for field in fields if field == 'employee' and not request.user.is_superuser}
        initial.update(request.GET.dict())

        form = modelform_factory(model, fields=fields)
        form = form(request.POST or None, request.FILES or None, initial=initial)

        if not request.user.is_superuser and 'employee' in form.fields:
            form.fields['employee'].widget.attrs['disabled'] = 'disabled'

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=self.get_inline_form_fields(inline), exclude=('metadata', 'created_by', 'updated_by'), can_delete=True, extra=1) for inline in formsets]
        formsets = [formset(queryset=formset.model.objects.none()) for formset in formsets]

        if not form.is_valid() or any(not formset.is_valid() for formset in formsets):
            for error in form.errors:
                messages.error(request, str(error))
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
        self.log(model, form, action=ADDITION, change_message=_('Ajout de {model} #{pk}').format(**{'model': model._meta.verbose_name, 'pk': form.instance.pk}))
        
        messages.add_message(request, messages.SUCCESS, message=_('Le {model} a été créé avec succès').format(**{'model': model._meta.model_name}))
        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)