from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms


def modelform_factory(model, fields='__all__', layout=None):
    """Factory to dynamically create a ModelForm for a given model with conditional layouts."""
    layout = layout or getattr(model, 'layout', layout or Layout())

    helper = FormHelper()
    helper.layout = layout

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
    form_class_name = f"{model._meta.model_name.capitalize()}ModelForm"
    form_class_attrs = {'Meta': Meta, 'helper': helper}

    return type(form_class_name, (forms.ModelForm,), form_class_attrs)