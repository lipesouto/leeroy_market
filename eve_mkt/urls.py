"""
URL configuration for eve_mkt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import path, include
from core.admin import admin_site
from core import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial pública
    path('home-logada/', views.home_logada, name='home_logada'),
    path('solicitar-nave/', views.solicitar_nave, name='solicitar_nave'),
    path('logout/', views.logout_view, name='logout'),
    path('eve-login/', views.login_eve, name='eve_login'),
    path('eve-callback/', views.eve_callback, name='eve_callback'),
    path('nave-autocomplete/', views.nave_autocomplete, name='nave_autocomplete'),
    path('admin/', admin_site.urls),
    path('perfil/', views.perfil, name='perfil'),
]
