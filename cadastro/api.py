from rest_framework import viewsets

from .models import User, Vagas
from .serializers import UserSerializer, VagaSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vagas.objects.all()
    serializer_class = VagaSerializer