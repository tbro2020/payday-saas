from django.utils.translation import gettext as _
from dal.autocomplete import ListSelect2
from crispy_forms.layout import Layout

from crispy_forms.helper import FormHelper
from django import forms

class InlineForm(forms.Form):
    class Meta:
        fields = '__all__'

    def __init__(self, args, kwargs):
        super(InlineForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class InlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'

def form_factory(model, fields):
    attrs = {'models': model}
    if fields: attrs['fields'] = fields

    class_name = str("%sForm" % model._meta.object_name)
    return type(class_name, (forms.Form,), fields)

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