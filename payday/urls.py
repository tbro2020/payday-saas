"""
URL configuration for payday project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('', include('core.urls')),
    path('api/', include('api.urls')),
    #path('payroll/', include('payroll.urls')),
    #path('employee/', include('employee.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('buple/', admin.site.urls))
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)