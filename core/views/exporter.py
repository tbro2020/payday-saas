from django.utils.translation import gettext as _
from core.filters import filter_set_factory
from django.shortcuts import HttpResponse
from django.utils.text import slugify
from django.shortcuts import render

from .base.base import BaseView
from django.apps import apps
from django.db import models
import pandas as pd



get_name_of_fields = lambda _list: list(map(lambda x: x.name, _list))

class Exporter(BaseView):
    action = ["view"]
    template_name = "export.html"
    
    def get_field_verbose(self, model, field):
        fields = field.split('__')
        if len(fields) == 1:
            return model._meta.get_field(fields[0]).verbose_name.lower()
        model = model._meta.get_field(fields[0]).related_model
        return self.get_field_verbose(model, '__'.join(fields[1:]))
    
    def get_field(self, model, field):
        fields = field.split('__')
        if len(fields) == 1:
            return model._meta.get_field(fields[0])
        model = model._meta.get_field(fields[0]).related_model
        return self.get_field(model, '__'.join(fields[1:]))
    
    def get_model_verbose_from_field(self, model, field):
        field = self.get_field(model, field)
        field = str(field).split('.')[:2]
        model = apps.get_model(*field)
        return model._meta.verbose_name.lower()
    
    def get(self, request, app, model):
        model = apps.get_model(app, model)
        return render(request, self.template_name, locals())
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        list_filter = getattr(model, 'list_filter', [])

        qs = model.objects.select_related().prefetch_related()
        qs = qs._all(user=request.user, subdomain=request.subdomain) if hasattr(qs, '_all') else qs.all()

        # apply hard filter based on fields
        groupBy = request.POST.get('groupBy', None)
        fields = [field.name for field in model._meta.fields]
        query = {k:v for k, v in request.GET.dict().items() if k.split('__')[0] in fields}
        query = {k: v for k, v in query.items() if v not in [None, 'unknown', 'true', 'false']}
        qs = qs.filter(**query)
        
        filter = filter_set_factory(model, fields=list_filter)
        qs = filter(request.GET, queryset=qs).qs

        fields = list({k:v for k,v in request.POST.dict().items() if k not in ['csrfmiddlewaretoken', 'groupBy']}.keys())
        if not fields: raise ValueError(_("Please select at least one field to export"))
        if groupBy and groupBy not in fields: fields = list(fields) + [groupBy]
        data = qs.values(*fields)

        fields = {field : f"{self.get_model_verbose_from_field(model, field)}.{self.get_field_verbose(model, field)}" 
                  for field in fields}

        df = pd.DataFrame.from_records(data).astype(str)
        df.rename(columns=fields, inplace=True)
        df.astype(str)
        
        filename = f"{slugify(model._meta.verbose_name)}.xlsx"
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with pd.ExcelWriter(response) as writer:
            if groupBy:
                for name, group in df.groupby(fields[groupBy]):
                    group.to_excel(writer, sheet_name=str(name), index=False)
            else:
                df.to_excel(writer, index=False)
        return response