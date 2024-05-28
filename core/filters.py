from django.utils.translation import gettext as _
from django.db.models import Q, CharField, TextField
from functools import reduce
import django_filters
from django import forms
from core import forms as core_forms

class AdvanceFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        field_name="q", 
        label="", 
        method='search_by_field', 
        widget=forms.TextInput(attrs={'class': 'd-none'})
    )
    
    def search_by_field(self, queryset, name, value):
        """
        Filters the queryset based on a search query applied to all CharField and TextField fields.
        """
        if not value.strip():
            return queryset
        
        model = self._meta.model
        fields = getattr(model, 'search_fields', [])
        
        # If no specific search fields are defined, use all CharField and TextField fields
        if not fields:
            fields = [field.name for field in model._meta.fields if isinstance(field, (CharField, TextField))]
        
        query = reduce(lambda q, field: q | Q(**{f"{field}__icontains": value}), fields, Q())
        return queryset.filter(query).distinct()

    def hard_filter(self):
        """
        Filters the queryset based on hard filters (all valid field filters in the request data).
        """
        query_params = {k: v for k, v in self.data.items() if v}
        valid_fields = {field.name for field in self._meta.model._meta.fields}

        filter_params = {k: v for k, v in query_params.items() if k.split("__")[0] in valid_fields}
        return self.queryset.filter(**filter_params)


def filter_set_factory(_model, fields):
    """
    Factory function to create a FilterSet class for the given model and fields.
    """
    attrs = {}
    _fields = fields
    
    # Create the Meta class for the FilterSet
    class Meta:
        model = _model
        fields = _fields

    for base_field in _fields:
        params = {}
        field_name, subfield = (base_field.split('__') + [None])[:2]
        
        try:
            field = _model._meta.get_field(field_name)
        except Exception as e:
            continue  # If the field does not exist, skip it

        if field.get_internal_type() in ['DateTimeField', 'DateField']:
            filter_class = django_filters.DateFromToRangeFilter if field.get_internal_type() == 'DateField' else django_filters.DateTimeFromToRangeFilter
            widget_class = core_forms.DateRangeWidget if field.get_internal_type() == 'DateField' else core_forms.DateTimeRangeWidget
            params['widget'] = widget_class()

            attrs[base_field] = filter_class(**params)

    attrs['Meta'] = Meta

    return type(f"{_model._meta.object_name}FilterSet", (AdvanceFilterSet,), attrs)
