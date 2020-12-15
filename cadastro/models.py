from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your models here.


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
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='curriculo')
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
