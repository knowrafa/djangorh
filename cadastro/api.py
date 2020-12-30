from rest_framework import viewsets
from .models import Usuario, Vagas
from .serializers import UserSerializer, VagaSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer


class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vagas.objects.all()
    serializer_class = VagaSerializer