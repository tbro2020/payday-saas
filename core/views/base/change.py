from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.http import Http404

from core.forms.button import Button
from django.urls import reverse_lazy
from django.contrib import messages
from django.apps import apps

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.admin.models import CHANGE
from django.db import transaction
from .base import BaseView
import copy


class Change(BaseView):
    next = None
    action = ["change"]
    template_name = "change.html"
    inline_formset_helper = InlineFormSetHelper()

    def get_action_buttons(self):
        obj = self._get_object()
        kwargs = {'app': self.kwargs['app'], 'model': self.kwargs['model']}

        _action_buttons = getattr(self.get_model(), 'get_action_buttons()', [])
        _action_buttons = [Button(**button) for button in _action_buttons]

        return [
            Button(**{
                'text': _('Cancel'),
                'tag': 'a',
                'url': reverse_lazy('core:list', kwargs=kwargs),
                'classes': 'btn btn-light-danger'
            }), 
            Button(**{
                'text': _('Delete'),
                'tag': 'a',
                'url': reverse_lazy('core:delete', kwargs=kwargs)+f'?pk__in={obj.pk}',
                'classes': 'btn btn-danger'
            }),
            Button(**{
                'text': _('Submit'),
                'tag': 'button',
                'classes': 'btn btn-success',
                'permission': 'add',
                'attrs': {
                    'type': 'submit',
                    'form': f'form-{kwargs["model"]}'
                }
            }),
        ] + _action_buttons
    
    def _get_object(self):
        model = self.get_model()
        pk = self.kwargs.get('pk', None)
        if not pk:
            raise Http404(_('Aucun identifiant n\'a été fourni'))
        return self.get_queryset().filter(**{model._meta.pk.name: pk}).first()

    def get(self, request, app, model, pk):
        model = self.get_model()
        obj = self._get_object()
        
        if not obj:
            message = _('Le {model} #{pk} n\'existe pas')
            messages.warning(request, message.format(**{'model': model._meta.model_name, 'pk': pk}))
            return redirect(reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        
        form = modelform_factory(model, fields=self.get_form_fields())
        form = form(instance=obj)
        form = self.filter_form(form)

        formsets = [formset(instance=obj) for formset in self.formsets()]
        return render(request, self.get_template_name(), locals())

    @transaction.atomic
    def post(self, request, app, model, pk):
        model = self.get_model()
        obj = self._get_object()

        instance = copy.copy(obj)
        
        form = modelform_factory(model, fields=self.get_form_fields())
        form = form(request.POST or None, request.FILES or None, instance=obj)
        form = self.filter_form(form)

        formsets = [formset(request.POST or None, request.FILES or None, instance=obj) for formset in self.formsets()]

        if not all(formset.is_valid() for formset in [form] + formsets):
            for error in form.errors: messages.warning(request, str(error))
            return render(request, self.get_template_name(), locals())

        form.save()
        [formset.save() for formset in formsets]

        message = _('Le {model} #{pk} a été mis à jour avec succès')
        self.log(model, form, action=CHANGE, change_message=self.generate_change_message(instance, form.instance))
        messages.add_message(request, messages.SUCCESS,  message=message.format(**{'model': model._meta.model_name, 'pk': pk}))

        redirect_to = reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name})
        return redirect(request.GET.dict().get('next', redirect_to))