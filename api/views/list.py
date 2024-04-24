from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import model_serializer_factory
from django.apps import apps

from rest_framework.metadata import SimpleMetadata

class List(APIView):
    metadata_class = SimpleMetadata
    
    def get(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        serializer = model_serializer_factory(model)

        qs = model.objects.all()
        serialized = serializer(qs, many=True)

        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)
        return Response({'status': 'success', 'data': serialized.data}, status=status.HTTP_200_OK)