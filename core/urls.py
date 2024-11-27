from django.views.decorators.cache import cache_page
from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create-organization', CreateOrganization.as_view(), name='create-organization'),
    path('password/change', PasswordChange.as_view(), name='password-change'),

    path('list/<str:app>/<str:model>', List.as_view(), name='list'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('read/<str:app>/<str:model>/<str:pk>', Read.as_view(), name='read'),
    path('change/<str:app>/<str:model>/<str:pk>', Change.as_view(), name='change'),
    path('delete/<str:app>/<str:model>/<str:pk>', Delete.as_view(), name='delete'),

    path('modal/list/<str:app>/<str:model>', ListModal.as_view(), name='list-modal'),
    path('modal/create/<str:app>/<str:model>', CreateModal.as_view(), name='create-modal'),
    path('modal/change/<str:app>/<str:model>/<str:pk>', ChangeModal.as_view(), name='change-modal'),
    path('modal/delete/<str:app>/<str:model>/<str:pk>', DeleteModal.as_view(), name='delete-modal'),
    
    path('print/<str:document>/<str:app>/<str:model>', Print.as_view(), name='print'),
    path('exporter/<str:app>/<str:model>', Exporter.as_view(), name='exporter'),
    path('notification/<str:pk>', Notification.as_view(), name='notification'),
    path('activity-log', ActivityLog.as_view(), name='activity-log'),

    path('canvas/download/<str:pk>', Canvas.as_view(), name='canvas-download'),
    path('action/required', ActionRequired.as_view(), name='action-required')
]
