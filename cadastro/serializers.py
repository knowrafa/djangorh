from django.contrib.auth.models import User, Group
from .models import Vagas
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff', 'password']


class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data):
        # create user
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


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