from django.db.models import Q, CharField, TextField
from django.utils.translation import gettext as _
from core.forms import DateRangeWidget
from functools import reduce
from django import forms
import django_filters

class AdvanceFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        label=str, 
        method='search', 
        widget=forms.TextInput(attrs={'class': 'form-control d-none'})
    )
    
    def search(self, queryset, name, value):
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
        return queryset.filter(query)

    def hard_filter(self):
        """
        Filters the queryset based on hard filters (all valid field filters in the request data).
        """
        # Extracting non-empty query parameters
        query_params = {k: v for k, v in self.data.items() if v}
        valid_fields = {field.name for field in self._meta.model._meta.fields}

        # Filtering parameters that correspond to valid fields
        filter_params = {
            k: v for k, v in query_params.items() if k.split("__")[0] in valid_fields
        }
        
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

    for field in _fields:
        field = _model._meta.get_field(field.split('__')[0])
        if field.get_internal_type() in ['DateTimeField', 'DateField']:
            attrs[field.name] = django_filters.DateFromToRangeFilter(**{
                'widget': DateRangeWidget()
            })

    attrs['Meta'] = Meta
    return type(f"{_model._meta.object_name}FilterSet", (AdvanceFilterSet,), attrs)
