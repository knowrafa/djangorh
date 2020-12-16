from django.contrib.auth.models import User, Group
from .models import Vagas
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff', 'password']


class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vagas
        fields = [
            "id",
            "nome",
            "descricao",
            "requisitos",
            "local",
            "faixa_salarial"
        ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']