"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from twitter import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('twitter.urls')),
    path('',include('django_messages.urls')),
    path('',include('django.contrib.auth.urls')),

    #password reset url's
    # path('password-reset/', auth_views.password_reset, name='password_reset'),
    # path('password-reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('password-reset/confirm/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.password_reset_complete, name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)