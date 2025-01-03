from rest_framework import viewsets
from django.apps import apps

from api.views.mixins import BaseApiMixin
from api.serializers import model_serializer_factory

class ApiViewSet(BaseApiMixin, viewsets.ModelViewSet):
    def get_serializer_class(self):
        depth = self.request.query_params.get('__depth', 0)
        return model_serializer_factory(self.get_model(), depth=int(depth))