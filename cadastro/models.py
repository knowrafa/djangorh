from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from rest_framework_api_key.models import APIKey


# Create your models here.

class Usuario(AbstractUser):
    chave = models.CharField(max_length=100, blank=True)
    chave_api = models.OneToOneField(APIKey, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if self.chave is None:
            object_key, key = APIKey.objects.create_key(name=self.username)
            self.chave = key
            self.chave_api = object_key
            print("Chave do usuario %s: %s" % (self.username, key))
        super(Usuario, self).save(*args, **kwargs)


# Criando uma API Key relacionada com um único usuário
# class ManageAPIKey(AbstractAPIKey):
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='api_key')


class Cadastro(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Curriculum(models.Model):
    INTERESSES_CHOICE = [
        ("Estágio", "Estágio"),
        ("CLT", "CLT"),
        ("PJ", "PJ"),
    ]
    # Choices dão opções para o usuário escolher ao preencher campos do banco de dados
    user = models.ForeignKey(to=Usuario, on_delete=models.DO_NOTHING, related_name='curriculo')
    interesess = models.CharField(max_length=255, choices=INTERESSES_CHOICE, default="Estágio")
    data_de_nascimento = models.DateField('Data de Nascimento')
    resumo = models.CharField(max_length=255)
    experiencia_profissional = models.TextField()
    cursos = models.TextField()
    idiomas = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name


class Vagas(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    requisitos = models.TextField()
    local = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
