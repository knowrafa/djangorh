"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import views as rest_views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from cadastro.api import UserViewSet, VagaViewSet

# ViewSets define the view behavior.

# Routers provide an easy way of automatically determining the URL conf.

api_router = routers.DefaultRouter()
api_router.register(r"user", UserViewSet)
api_router.register(r"vagas", VagaViewSet)

urlpatterns = [
    path('', views.main_page, name='principal'),
    path('home/', views.HomePageUserView.as_view(), name='home'),
    path('second/', views.second_page, name='second'), # Página exemplo
    path('admin/', admin.site.urls), # Página da administração
    path('api-vagas/', include(api_router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Rest Framework API Authentication, com login e logout
    path('cadastro/', include('cadastro.urls')),
    path('vagas/', views.VagasList.as_view(), name="ver_vagas"), # Utilizando o padrão resto na view VagasList
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # Deixando explícito o nome do template (argumentos não necessários)
    # path('logout/', views.logout_page, name="logout"),
    path('logout/', views.LogoutUser.as_view(), name='logout'), # View padrão de logout do Django
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns = format_suffix_patterns(urlpatterns)
