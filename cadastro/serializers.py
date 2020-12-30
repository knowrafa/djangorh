from django.contrib.auth.models import Group
from django.db import transaction

from .models import Vagas, Usuario
from rest_framework import serializers


# class ManageApiKeySerializer(serializers.ModelSerializer):
#
#     # Guardando chave
#     # key = serializers.SerializerMethodField(method_name='create')
#
#     class Meta:
#         model = ManageAPIKey
#         fields = [
#             'user',
#             'name',
#             # 'key',
#         ]
#
#         # @staticmethod
#         def create(self, validated_data):
#             # Cria a key, baseado no usuário e no nome dele recebido
#             _, generated_key = ManageAPIKey.objects.create_key(**validated_data)
#             user_instance = User.objects.filter(username=validated_data['name'])
#             print("chama o update")
#             self.update(username=validated_data['name'], key=generated_key)
#             return generated_key
#
#         @staticmethod
#         def update(username, **kwargs):
#             print("Como funciona o kwargs: ")
#             print(kwargs)
#             # Utiliza os próximos argumentos para atualizar a apikey
#             for field, value in kwargs:
#                 print(field, value)
#                 try:
#                     ManageAPIKey.objects.filter(name=username).update(field=value)
#                 except:
#                     break
#             pass


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'url', 'username', 'email', 'is_staff', 'password']


class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

    @transaction.atomic
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
    # def create(self, validated_data) -> bool:
    #     # create user
    #     try:
    #         # !TODO Verificar se preciso implementar ou posso enviar já desconstruído
    #         # Desconstrói o dicionário validated data e cria o usuário
    #         # Caso dê erros retorna um serializer.error
    #         user = User.objects.create_user(**validated_data)
    #     except:
    #         print("falhou chefe")
    #     else:
    #         # salvando usuário
    #         user.save()
    #         return True
    #     return False
    # 


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


# Acho que isso não funciona agora
class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    email = serializers.EmailField()


# Acho que isso não funciona agora
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
