from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Cadastro(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="cadastro")

    def __str__(self):
        return self.nome


class Curriculum(models.Model):
    INTERESSES_CHOICE = [
        ("Estágio", "Estágio"),
        ("CLT", "CLT"),
        ("PJ", "PJ"),
    ]
    # Choices dão opções para o usuário escolher ao preencher campos do banco de dados
    cadastro = models.ForeignKey(Cadastro, on_delete=models.DO_NOTHING, related_name='curriculo')
    nome = models.CharField(max_length=255)
    interesess = models.CharField(max_length=255, choices=INTERESSES_CHOICE, default="Estágio")
    email = models.CharField(max_length=255)
    data_de_nascimento = models.DateField('Data de Nascimento')
    resumo = models.CharField(max_length=255)
    experiencia_profissional = models.TextField()
    cursos = models.TextField()
    idiomas = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Vagas(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    requisitos = models.TextField()
    local = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
