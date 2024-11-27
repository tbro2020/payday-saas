from core.filters import filter_set_factory
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.apps import apps
from .base import BaseView

get_name_of_fields = lambda _list: list(map(lambda x: x.name, _list))

class List(BaseView):
    action = ["view"]
    template_name = "list.html"

    def get_queryset_actions(self):
        app, model = self.kwargs['app'], self.kwargs['model']
        model = apps.get_model(app, model_name=model)
        return [{
            'title': getattr(action, 'short_description'),
            'name': getattr(action, '__name__')
        } for action in getattr(model, 'actions', [])]

    def get_list_display(self, model):
        list_display = getattr(model, 'list_display', [])
        list_display_order = {field: i for i, field in enumerate(list_display)}
        return sorted([field for field in model._meta.fields if field.name in list_display], key=lambda field: list_display_order[field.name])
    
    def get_list_filter(self, model):
        return getattr(model, 'list_filter', [])

    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        if hasattr(model, 'list_url'):
            return redirect(getattr(model, 'list_url'))

        list_display = self.get_list_display(model)
        list_filter = self.get_list_filter(model)

        # get queryset based on user 
        qs = model.objects.all()
        if hasattr(model.objects, 'related_to'):
            qs = model.objects.related_to(user=request.user)
        
        # select and prefetch related
        qs = qs.select_related().prefetch_related()

        # apply hard filter based on fields
        fields = [field.name for field in model._meta.fields]
        query = {k:v for k, v in request.GET.dict().items() if k.split('__')[0] in fields}
        query = {k: v for k, v in query.items() if v not in [None, 'unknown', 'true', 'false']}
        qs = qs.filter(**query)

        # apply soft filter based on list_filter
        filter = filter_set_factory(model, fields=list_filter)
        filter = filter(request.GET, queryset=qs)
        qs = filter.qs

        paginator = Paginator(qs.order_by('-id'), 100)
        qs = paginator.page(int(request.GET.dict().get('page', 1)))
        return render(request, getattr(model, "change_list_template", self.template_name), locals())