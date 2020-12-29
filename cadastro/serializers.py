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
        try:
            print(validated_data)
            user = User.objects.create(**validated_data)
            """
                user = User.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=validated_data['password'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                )
            """
        except:
            print("falhou chefe")
        else:
            # salvando usuário
            user.save()
            return True

        return False


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


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    email = serializers.EmailField()



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']