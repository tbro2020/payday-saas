from django.urls import path
from employee.views import *

app_name = 'employee'

urlpatterns = [
    path('change/<int:pk>', Employee.as_view(), name='change'),
]
