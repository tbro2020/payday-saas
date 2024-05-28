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
        } for action in model.actions]

    def get_list_display(self, model):
        list_display = getattr(model, 'list_display', [])
        return [field for field in model._meta.fields if field.name in list_display]
    
    def get_list_filter(self, model):
        list_filter = getattr(model, 'list_filter', [])
        return [field for field in model._meta.fields if field.name in list_filter]

    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)

        if hasattr(model, 'list_url'):
            return redirect(getattr(model, 'list_url'))

        list_display = self.get_list_display(model)
        list_filter = self.get_list_filter(model)

        qs = model.objects._all(
            subdomain=request.subdomain
        ).select_related().prefetch_related() if hasattr(model, '_all') else model.objects.all()
        
        filter = filter_set_factory(model, fields=get_name_of_fields(list_filter))
        filter = filter(request.GET, queryset=qs)

        paginator = Paginator(filter.hard_filter(), 25)
        qs = paginator.page(int(request.GET.dict().get('page', 1)))
        return render(request, getattr(model, "change_list_template", self.template_name), locals())