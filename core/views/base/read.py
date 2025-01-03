from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.http import Http404

from core.forms import modelform_factory, InlineFormSetHelper, Button
from django.urls import reverse_lazy
from django.contrib import messages
from .base import BaseView


class Read(BaseView):
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
            })
        ] + _action_buttons
    
    def _get_object(self):
        model = self.get_model()
        pk = self.kwargs.get('pk', None)
        if not pk:
            raise Http404(_('Aucun identifiant n\'a été fourni'))
        return self.get_queryset().filter(**{model._meta.pk.name: pk}).first()
    
    def _set_readonly_and_class(self, fields, readonly=True, css_class='bg-dark'):
        for field in fields:
            field.widget.attrs['readonly'] = readonly
            field.widget.attrs['class'] = css_class

    def get(self, request, app, model, pk):
        model = self.get_model()
        obj = self._get_object()
        
        if not obj:
            message = _('Le {model} #{pk} n\'existe pas')
            messages.warning(request, message.format(**{'model': model._meta.model_name, 'pk': pk}))
            return redirect(reverse_lazy('core:list', kwargs={'app': app, 'model': model._meta.model_name}))
        
        self.inline_formset_helper.form_tag = False
        form = modelform_factory(model, fields=self.get_form_fields(), form_tag=False)
        
        form = form(instance=obj)
        form = self.filter_form(form)
        self._set_readonly_and_class(form.fields.values())

        formsets = [formset(instance=obj) for formset in self.formsets()]

        for formset in formsets:
            for form in formset:
                for field in form.fields:
                    self._set_readonly_and_class(form.fields.values())

        return render(request, self.get_template_name(), locals())