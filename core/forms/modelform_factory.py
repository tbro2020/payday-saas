from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms


def modelform_factory(model, fields=None, layout=None, form_class_name=None, form_tag=True):
    """Factory to dynamically create a ModelForm for a given model with conditional layouts."""
    layout = layout or getattr(model, 'layout', Layout())

    helper = FormHelper()
    helper.layout = layout
    helper.form_tag = form_tag

    # Define Meta class with fields and exclusions
    Meta = type(
        'Meta', 
        (object,), 
        {
            'model': model,
            'fields': fields or '__all__',
        }
    )

    # Create the ModelForm class dynamically
    form_class_name = form_class_name or f"{model._meta.model_name.capitalize()}ModelForm"
    form_class_attrs = {'Meta': Meta, 'helper': helper, 'form_tag': 'form' if helper.form_tag else 'div'}

    return type(form_class_name, (forms.ModelForm,), form_class_attrs)