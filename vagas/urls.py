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
from django.urls import path, include
from . import views

# Lembrar o motivo de dar nome para o app
app_name = 'vagas'
urlpatterns = [
    path('', views.VagasList.as_view(), name="vagas"),
    path('api/', views.ApiVagasList.as_view(), name="api de vagas")
    # path("api/", include(api_router.urls)),
    # Ainda não entendi o que significa
    # path('', include(router.urls)),
    # path("api-auth/", include('rest_framework.urls', namespace='rest_framework'))
    # path('<int:pagina_id>/', views.cadastrar, name="cadastro"),
]