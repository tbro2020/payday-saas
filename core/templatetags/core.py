from django.apps import apps
from django import template
import re

from django.core.cache import cache
from django.shortcuts import render

from django.utils.safestring import mark_safe
from django import template
import re

from django import template
import re

from datetime import timedelta
import qrcode.image.svg
from io import BytesIO
import qrcode
import base64


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
def qs_to_table(obj, app, model, *args, **kwargs):
    qs = apps.get_model(app, model).objects.all()
    fields = kwargs.get('fields', '').split(',')

    _filter = eval(kwargs.get('filter', '{}'))
    qs = qs.filter(**_filter)

    fields = [field for field in qs.model._meta.fields if field.name in fields]
    return mark_safe(render(None, 'components/qs_to_table.html', locals()).content.decode('utf-8'))

@register.filter('cache_get')
def cache_get(key):
    return cache.get(key)

@register.simple_tag
def watermarker(message):
    message = f"""<div class="watermark">
        <h1 class="watermark-title-text">{ message }</h1>
    </div>"""
    return mark_safe(message)

@register.simple_tag
def table(qs, *args):
    def _rows(obj):
        return ["<td>{value}</td>".format(value=getattr(obj, field.name, None)) 
                for field in obj._meta.fields if field.name in args]
    
    rows = ''.join(["<tr><td>{idx}</td>{rows}</tr>".format(idx=idx+1, rows=''.join(_rows(obj))) for idx, obj in enumerate(qs)])
    headers = ''.join(["<th>#</th>"]+["<th>{field}</th>".format(field=field.verbose_name.title()) 
               for field in qs.model._meta.fields if field.name in args])
    
    table = """<table class='table table-striped'>
                <thead><tr>{header}</tr></thead>
                <tbody>{body}</tbody>
            <table>""".format(header=headers, body=rows)
    return mark_safe(table)

@register.filter(name="atmQrcode")
def atmQrcode(operation, product):
    factory = qrcode.image.svg.SvgImage
    content = "{'next':'atm', 'operation': %d, 'product': %d}" % (operation, product)
    img = qrcode.make(content, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    base64_image = base64.b64encode(stream.getvalue()).decode()
    return 'data:image/svg+xml;utf8;base64,' + base64_image

@register.filter(name="addDays")
def addDays(date, days):
    return date + timedelta(days=days)


@register.filter(name='qs_sum_of')
def qs_sum_of(qs, field):
    return sum([getattr(obj, field, 0) for obj in qs])

@register.filter(name='qs_limit')
def qs_limit(qs, limit):
    if not qs: return qs
    return qs[:limit]