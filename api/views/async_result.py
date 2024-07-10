from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from celery import result

class AsyncResult(APIView):
    def get(self, request, id):
        return Response(result.AsyncResult(id).get(), status=status.HTTP_200_OK)