from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('list/<str:app>/<str:model>', List.as_view(), name='list'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('detail/<str:app>/<str:model>/<int:pk>', Detail.as_view(), name='detail'),
    path('autocomplete/<str:app>/<str:model>/<str:to_field>', Autocomplete.as_view(), name='autocomplete')
]
