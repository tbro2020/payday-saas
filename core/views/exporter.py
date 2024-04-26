from django.utils.translation import gettext as _
from core.filters import filter_set_factory
from django.shortcuts import HttpResponse
from django.shortcuts import render

from django.apps import apps
from .base.base import BaseView
import pandas as pd

class Exporter(BaseView):
    action = ["view"]
    
    def get(self, request, app, model):
        model = apps.get_model(app, model)
        return render(request, "export.html", locals())
    
    def post(self, request, app, model):
        model = apps.get_model(app, model)
        list_filter = getattr(model, 'list_filter', [])

        qs = model.objects.select_related().prefetch_related()
        qs = qs._all(user=request.user) if hasattr(qs, '_all') else qs.all()

        # Hard filter
        query = {k:v for k, v in request.GET.dict().items() if v}
        fields = [field.name for field in model._meta.fields if field.name]
        qs = qs.filter(**{k:v.split(',') if k.split('__')[-1] == 'in' else v 
            for k, v in query.items() if k.split("__")[0] in fields})
        
        filter = filter_set_factory(model, fields=list_filter)
        qs = filter(request.GET, queryset=qs)
        qs = qs.qs.order_by('-id')

        fields = {k:v for k,v in request.POST.dict().items() if k not in ['csrfmiddlewaretoken']}.keys()
        data = [{field.replace('__', '.'): str(getattr(obj, field, None)) for field in fields} for obj in qs]

        df = pd.DataFrame.from_records(data)
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="{model._meta.verbose_name}.xlsx"'

        with pd.ExcelWriter(response) as writer:
            df.to_excel(writer)
        return response