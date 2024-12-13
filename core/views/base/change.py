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
import copy


class Change(BaseView):
    next = None
    action = ["change"]
    template_name = "change.html"
    inline_formset_helper = InlineFormSetHelper()

    def can_change(self, obj=None):
        # Superusers and staff can change anything
        user = self.request.user
        if user.is_superuser or user.is_staff: return True

        app, model = self.kwargs['app'], self.kwargs['model']
        model = apps.get_model(app, model_name=model)
        
        if not obj:
            obj = get_object_or_404(model, **{model._meta.pk.name: self.kwargs['pk']})

        # If the object is already approved, no one can change it
        if obj.approved: return False

        # If the object is not approved, only the creator and the approvers can change it
        approbations = self.approbations()
        actions = list(approbations.values())

        # Creator can't change his own object if it's already approved
        if actions and user == obj.created_by: 
            return False

        # If the user is not in the list of approvers, he can't change the object
        actors = list(approbations.keys())
        actors.append(obj.created_by.email)

        return user.email in actors

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, **{model._meta.pk.name: pk})
        fields = self.get_form_fields(model)

        if not self.can_change(obj=obj):
            messages.warning(request, _('Vous n\'avez pas permission d\'effectuer cette action'))
            return redirect(reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        
        form = modelform_factory(model, fields=fields)
        form = form(instance=obj)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=self.get_inline_form_fields(inline), exclude=('metadata', 'created_by', 'updated_by'), can_delete=False, extra=1) for inline in formsets]
        formsets = [formset(instance=obj) for formset in formsets]
        
        return render(request, self.template_name, locals())

    def post(self, request, app, model, pk):
        model = apps.get_model(app, model)

        obj = get_object_or_404(model, pk=pk)
        fields = self.get_form_fields(model)
        instance = copy.copy(obj)
        
        form = modelform_factory(model, fields=fields)
        form = form(request.POST or None, request.FILES or None, instance=obj)

        formsets = [apps.get_model(inline.split('.')[0], model_name=inline.split('.')[-1]) for inline in getattr(model, 'inlines', [])]
        formsets = [inlineformset_factory(model, inline, fields=self.get_inline_form_fields(inline), exclude=('metadata', 'created_by', 'updated_by'), can_delete=False, extra=1) for inline in formsets]
        formsets = [formset(request.POST or None, request.FILES or None, instance=obj) for formset in formsets]

        if not form.is_valid() or False in [formset.is_valid() for formset in formsets]:
            for error in form.errors: messages.error(request, str(error))
            return render(request, self.template_name, locals())

        form.save()
        [formset.save() for formset in formsets]

        self.log(model, form, action=CHANGE, change_message=self.generate_change_message(instance, form.instance))
        messages.add_message(request, messages.SUCCESS,  message=_('Le {model} #{pk} a été mis à jour avec succès').format(**{'model': model._meta.model_name, 'pk': pk}))

        next = request.GET.dict().get('next', reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        return self.next if self.next else redirect(next)