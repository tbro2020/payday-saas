from django.utils.translation import gettext as _
from dal.autocomplete import ListSelect2
from crispy_forms.layout import Layout

from crispy_forms.helper import FormHelper
from django import forms

def modelform_factory(model, fields, layout=Layout()):
    attrs = {'model': model}
    if fields: attrs['fields'] = fields

    attrs['widgets'] = {field.name: ListSelect2() for field in model._meta.fields if field.choices}
    Meta = type(str('Meta'), (object,), attrs)

    helper = FormHelper()
    attrs = {'Meta': Meta}
    helper.layout = layout or getattr(model, 'layout', layout)
            
    attrs['helper'] = helper
    class_name = str("%sModelForm" % model._meta.object_name)
    return type(class_name, (forms.ModelForm,), attrs)