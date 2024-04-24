from django.utils.translation import gettext as _
from django.db.models import Q
from functools import reduce
from django_filters import *
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

    for field in model._meta.fields:
        if field.name not in fields: continue
        if field.get_internal_type() not in ['DateTimeField', 'DateField']: continue
        _class = eval(field.get_internal_type().replace("Field", "FromToRangeFilter"))
        attrs[field.name] = _class(help_text=_('YYYY-MM-DD'))
    
    attrs['Meta'] = meta
    return type(str("%sFilterSet" % model._meta.object_name), (AdvanceFilterSet,), attrs)
