from django import template
import re

from django.utils.safestring import mark_safe
from django.shortcuts import render


digital_value = re.compile(r"\d+")
register = template.Library()

@register.filter('getattr')
def getattribute(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'get') and value.get(arg):
        return value[arg]
    elif digital_value.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    return None

@register.filter('qs_to_values')
def qs_to_values(qs, field):
    return list(qs.values(*field.split(',')))


@register.filter('toint')
def toint(value):
    return int(value)

@register.simple_tag
def qs_to_table(qs, fields, css_class='table table-striped', *args, **kwargs):
    fields = fields.split(',')

    fields = [field for field in qs.model._meta.fields if field.name in fields]
    return render(None, 'components/qs_to_table.html', locals()).content.decode('utf-8')