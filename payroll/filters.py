from django.utils.translation import gettext as _
from django.db.models import Q
from functools import reduce
from django_filters import *

from core import forms as core_forms
from django import forms


class AdvanceFilterSet(FilterSet):
    q = CharFilter("", label="", method='search', widget=forms.TextInput(attrs={'class': 'd-none'}))
    
    def search(self, queryset, name, value):
        fields = getattr(self._meta.model, 'search_fields', [])
        fields = fields if fields else [field.name for field in self._meta.model._meta.fields if field.get_internal_type() in ['CharField', 'TextField']]
        return queryset.filter(reduce(lambda q, field: q | Q(**{f'{field}__icontains': value}), fields, Q()))

    def hard_filter(self):
        query = {k:v for k, v in self.data.items() if v}
        fields = [field.name for field in self._meta.model._meta.fields if field.name]
        return self.queryset.filter(**{k:v for k, v in query.items() if k.split("__")[0] in fields})


def filter_set_factory(model, fields):
    attrs = {}
    meta = type(str("Meta"), (object,), {"model": model, "fields": fields})

    for base_field in fields:
        params = {}
        field, subfield = base_field.split('__') if '__' in base_field else (base_field, None)
        field = model._meta.get_field(field)

        if field.get_internal_type() not in ['DateTimeField', 'DateField']: continue
        _class = eval(field.get_internal_type().replace("Field", "FromToRangeFilter"))
  
        if _class.__name__.endswith('ToRangeFilter'):
            base_class_name = _class.__name__.replace('FromToRangeFilter', '')
            params['widget'] = getattr(core_forms, f'{base_class_name}RangeWidget')()
        attrs[base_field] = _class(**params)
        
    
    attrs['Meta'] = meta
    return type(str("%sFilterSet" % model._meta.object_name), (AdvanceFilterSet,), attrs)
