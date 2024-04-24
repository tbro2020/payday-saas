from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.forms import inlineformset_factory
from crispy_forms.layout import Layout
from django.apps import apps

from core.forms import modelform_factory, InlineFormSetHelper
from .base import BaseView


class Read(BaseView):
    next = None
    action = ["view"]
    template_name = "read.html"
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