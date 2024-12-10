from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('autocomplete/<str:app>/<str:model>/<str:to_field>', Autocomplete.as_view(), name='autocomplete'),
    path('detail/<str:app>/<str:model>/<int:pk>', Detail.as_view(), name='detail'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('list/<str:app>/<str:model>', List.as_view(), name='list')
]
