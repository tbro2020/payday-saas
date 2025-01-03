from django.views.decorators.cache import cache_page
from django.conf.urls.i18n import set_language
from django.contrib.auth import views
from django.urls import path
from core.views import *

app_name = 'core'


class LogoutView(views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('create-organization', CreateOrganization.as_view(), name='create-organization'),
    path('password/change', PasswordChange.as_view(), name='password-change'),

    path('list/<str:app>/<str:model>', List.as_view(), name='list'),
    path('create/<str:app>/<str:model>', Create.as_view(), name='create'),
    path('delete/<str:app>/<str:model>', Delete.as_view(), name='delete'),
    path('read/<str:app>/<str:model>/<str:pk>', Read.as_view(), name='read'),
    path('change/<str:app>/<str:model>/<str:pk>', Change.as_view(), name='change'),

    path('modal/list/<str:app>/<str:model>', ListModal.as_view(), name='list-modal'),
    path('modal/create/<str:app>/<str:model>', CreateModal.as_view(), name='create-modal'),
    path('modal/delete/<str:app>/<str:model>', DeleteModal.as_view(), name='delete-modal'),
    path('modal/change/<str:app>/<str:model>/<str:pk>', ChangeModal.as_view(), name='change-modal'),
    
    path('print/<str:document>/<str:app>/<str:model>', Print.as_view(), name='print'),
    path('exporter/<str:app>/<str:model>', Exporter.as_view(), name='exporter'),
    path('notification/<str:pk>', Notification.as_view(), name='notification'),
    path('activity-log', ActivityLog.as_view(), name='activity-log'),

    path('canvas/download/<str:pk>', Canvas.as_view(), name='canvas-download'),
    path('action/required', ActionRequired.as_view(), name='action-required')
]
