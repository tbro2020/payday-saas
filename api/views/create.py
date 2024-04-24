from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import model_serializer_factory
from rest_framework.metadata import SimpleMetadata
from django.apps import apps
    
from employee.models import Employee
from datetime import date, datetime

class Create(APIView):
    metadata_class = SimpleMetadata

    def post(self, request, app, model):
        model = apps.get_model(app, model_name=model)
        serializer = model_serializer_factory(model, depth=0)
        
        data = request.data
        employee = Employee.objects.get(registration_number=data.pop('registration_number')).id
        data['employee'] = employee
        data['date'] = date.today()
        data['time'] = str(datetime.now()).split(' ')[1].split('.')[0]

        serialized = serializer(data=data)
        if not serialized.is_valid():
            return Response({'status': 'unsuccessful', 'data': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        serialized.save()

        #meta = self.metadata_class()
        #data = meta.get_serializer_info(serialized)

        serializer = model_serializer_factory(model)
        serialized = serializer(serialized.instance)
        return Response({'status': 'success', 'data': serialized.data}, status=status.HTTP_201_CREATED)