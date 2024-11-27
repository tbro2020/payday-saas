from django.db.models import Q
from django.apps import apps
from dal import autocomplete

from django.conf import settings
from functools import reduce


class Autocomplete(autocomplete.Select2QuerySetView):

    def get_model(self, app, model):
        try:
            return apps.get_model(app, model_name=model)
        except Exception as ex:
            apps.get_app_config('core').apps.register_model('core', model)
            return apps.get_model(app, model_name=model)

    def get_queryset(self):
        model = self.get_model(self.kwargs.get('app'), self.kwargs.get('model'))

        if not self.request.user.is_authenticated:
            return model.objects.none()

        qs = model.objects.all()
        fields = [field.name for field in model._meta.fields if field.get_internal_type() in ['CharField', 'TextField']]
        return qs.filter(reduce(lambda q, field: q | Q(**{f'{field}__icontains': self.q}), fields, Q())).order_by('-id')

    def get_result_value(self, result):
        return getattr(result, self.kwargs.get('to_field', 'pk'), result)
