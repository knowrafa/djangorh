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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', views.main_page, name='principal'),
    path('home/', views.homepage, name='home'),
    path('second/', views.second_page, name='second'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # Rest Framework API
    path('cadastro/', include('cadastro.urls')),
    path('vagas/', views.ver_vagas, name="ver_vagas"),
    # path('login/', include('login.urls')),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_page, name="logout")
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)