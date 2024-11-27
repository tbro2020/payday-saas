from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import model_serializer_factory
from django.shortcuts import get_object_or_404
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
    

class Create(APIView):
    metadata_class = SimpleMetadata

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        serializer = model_serializer_factory(model, depth=0)
        print(request.data)
        
        serialized = serializer(data=request.data)
        if not serialized.is_valid():
            return Response({'status': 'unsuccessful', 'data': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        serialized.save()

        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)

        serializer = model_serializer_factory(model)
        serialized = serializer(serialized.instance)
        return Response({'status': 'success', 'data': serialized.data}, status=status.HTTP_201_CREATED)

class Detail(APIView):
    metadata_class = SimpleMetadata

    def get(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        serializer = model_serializer_factory(model)

        obj = get_object_or_404(model, pk=pk)
        serialized = serializer(obj)

        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)
        return Response({'status': 'success', 'data': serialized.data})
    
    def put(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        serializer = model_serializer_factory(model, depth=0)

        obj = get_object_or_404(model, pk=pk)
        serialized = serializer(obj, data=request.data, partial=True)
        if not serialized.is_valid():
            return Response({'status': 'unsuccessful', 'data': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        serialized.save()
        
        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)

        serializer = model_serializer_factory(model)
        serialized = serializer(serialized.instance)
        return Response({'status': 'success', 'data': serialized.data})
    
    def delete(self, request, app, model, pk):
        model = apps.get_model(app, model_name=model)
        obj = get_object_or_404(model, pk=pk)
        obj.delete()

        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)
        return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)