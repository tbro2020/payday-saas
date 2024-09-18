from django.urls import path
from employee.views import *

app_name = 'employee'

urlpatterns = [
    path('change/<str:pk>', Employee.as_view(), name='change'),
    path('sheet/<str:pk>', Sheet.as_view(), name='sheet'),
]
