from django.contrib.auth.models import User, Group
from .models import Vagas
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vagas
        fields = [
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