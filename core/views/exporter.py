from django.utils.translation import gettext as _
from core.filters import filter_set_factory
from django.shortcuts import HttpResponse
from django.shortcuts import render

from django.apps import apps
from .base.base import BaseView
import pandas as pd

get_name_of_fields = lambda _list: list(map(lambda x: x.name, _list))

class Exporter(BaseView):
    action = ["view"]

    def get_list_display(self, model):
        list_display = getattr(model, 'list_display', [])
        return [field for field in model._meta.fields if field.name in list_display]
    
    def get_list_filter(self, model):
        list_filter = getattr(model, 'list_filter', [])
        return [field for field in model._meta.fields if field.name in list_filter]
    
    def get(self, request, app, model):
        model = apps.get_model(app, model)
        return render(request, "export.html", locals())
    
    def get_field_verbose(self, field, subfield):
        if field.is_relation and subfield != field.name:
            return ".".join([field.verbose_name, field.related_model._meta.get_field(subfield).verbose_name]).lower()
        return field.verbose_name.lower()
    
    def nested_getattr(self, obj, attr, default=None):
        """
        Recursively get attributes.
        Example: nested_getattr(person, 'address.city') is equivalent to person.address.city
        """
        attributes = attr.split('.')
        for attribute in attributes:
            obj = getattr(obj, attribute, default)
        return obj
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        list_filter = self.get_list_filter(model)

        qs = model.objects.select_related().prefetch_related()
        qs = qs._all(user=request.user, subdomain=request.subdomain) if hasattr(qs, '_all') else qs.all()
        
        filter = filter_set_factory(model, fields=get_name_of_fields(list_filter))
        qs = filter(request.GET, queryset=qs).qs

        pk = model._meta.pk.name
        fields = [field.name for field in model._meta.fields]
        
        qs = qs.filter(**{k.replace('pk', pk) if k.split('__')[0] == 'pk' else k:v.split(',') if '__in' in k else v
                        for k,v in request.GET.dict().items() if k.split('__')[0].replace('pk', pk) in fields})

        fields = {k:v for k,v in request.POST.dict().items() if k not in ['csrfmiddlewaretoken']}.keys()
        data = qs.values(*fields)

        fields = {field : 
                self.get_field_verbose(model._meta.get_field(field.split('__')[0]), field.split('__')[-1]) 
                for field in fields}

        df = pd.DataFrame.from_records(data)
        df.rename(columns=fields, inplace=True)
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="{model._meta.verbose_name}.xlsx"'

        with pd.ExcelWriter(response) as writer:
            df.to_excel(writer)
        return response