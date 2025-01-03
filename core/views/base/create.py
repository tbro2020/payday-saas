from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib import messages

from core.forms import modelform_factory, InlineFormSetHelper
from django.contrib.admin.models import ADDITION
from django.shortcuts import render, redirect
from core.forms.button import Button
from django.urls import reverse_lazy
from django.db import transaction
from .base import BaseView





class Create(BaseView):
    next = None
    action = ["add"]
    template_name = "create.html"
    inline_formset_helper = InlineFormSetHelper()

    def get_action_buttons(self):
        kwargs = {'app': self.kwargs['app'], 'model': self.kwargs['model']}
        return [
            Button(**{
                'text': _('Cancel'),
                'tag': 'a',
                'url': reverse_lazy('core:list', kwargs=kwargs),
                'classes': 'btn btn-light-danger',
                'permission': 'delete'
            }), Button(**{
                'text': _('Submit'),
                'tag': 'button',
                'classes': 'btn btn-success',
                'permission': 'add',
                'attrs': {
                    'type': 'submit',
                    'form': f'form-{kwargs["model"]}'
                }
            })
        ]

    def get(self, request, app, model):
        model = self.get_model()
        
        form = modelform_factory(model, fields=self.get_form_fields())
        form = form(initial=request.GET.dict())
        form = self.filter_form(form)

        formsets = [formset() for formset in self.formsets()]
        return render(request, self.get_template_name(), locals())
    
    @transaction.atomic
    def post(self, request, app, model):
        model = self.get_model()
        
        form = modelform_factory(model, fields=self.get_form_fields())
        form = form(request.POST or None, request.FILES or None)
        form = self.filter_form(form)

        formsets = [formset(request.POST or None, request.FILES or None) for formset in self.formsets()]

        if not all(formset.is_valid() for formset in [form] + formsets):
            for error in form.errors: messages.warning(request, str(error))
            return render(request, self.get_template_name(), locals())

        instance = form.save()
        for formset in formsets:
            instances = formset.save(commit=False)
            for obj in instances:
                setattr(obj, formset.fk.name, instance)
                obj.save()

        message = _('Ajout du/de {model} #{pk}')
        self.log(model, form, action=ADDITION, change_message=self.generate_change_message(instance, form.instance))
        messages.add_message(request, messages.SUCCESS,  message=message.format(**{'model': model._meta.model_name, 'pk': instance.pk}))

        redirect_to = reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name})
        return redirect(request.GET.dict().get('next', redirect_to))