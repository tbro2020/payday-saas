from django.utils.translation import gettext as _
from django import forms


def form_factory(model, fields):
    attrs = {'models': model}
    if fields: attrs['fields'] = fields

    class_name = str("%sForm" % model._meta.object_name)
    return type(class_name, (forms.Form,), fields)