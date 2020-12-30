from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import *
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CadastroForm
from .models import Vagas
from .serializers import CadastroSerializer

import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

def index(request):
    response = "Página de index"
    return HttpResponse(response)


# Cadastro com Rest Framework API
class CadastrarUsuario(APIView):
    """
        Lista todas as vagas, utilizando APIView
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # Se estiver Autenticado pode realizar POST, se não pode apenas realizar GET
    # permission_classes = [IsAuthenticated]

    # Identificando que a interface dessa url será um html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cadastro/cadastro.html'

    # @login_required DOESNT WORK HERE!!
    @staticmethod
    def get(request):
        # Verificando autenticação do usuário e redirecionando à página de login
        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")
        return Response()

    @staticmethod
    def post(request):
        # Encaixa o 'data' da requisição no serializer correspondente
        serializer = CadastroSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid:
            user = serializer.save()
            login(request, user)
            return HttpResponseRedirect(redirect_to='/')
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            # !TODO Testar se o serializer fica válido com mais informações do que o necessário
            # Verifica se o create funciona (retorna True ou False - Método sobrescrito)
            # if serializer.create(validated_data=serializer.data):
            #     username = serializer.data['username']
            #     user = User.objects.get(username=username)
            #     token = request.data['csrfmiddlewaretoken']
            # Montando o data manualmente
            # api_data = {'csrfmiddlewaretoken': [token], 'user': [user], 'name': [user.username]}

            # print(request.data)
            # api_serializer = ManageApiKeySerializer(data=api_data)
            # print(api_serializer)
            # print(api_serializer.is_valid())
            # logging.debug("validooouuuuu ou não rsrsrs")
            # api_data['key'] = api_serializer.create(validated_data=api_serializer.data)

            # Criando API KEY com base no usuário e com OneToOneField (o user é único)
            # _, generated_key = ManageAPIKey.objects.create_key(user=user, name=user.username)

            # No dado modelo API Key, a chave guardada e permitida no Django admin é apenas o prefixo
            # key_split, _ = generated_key.split(".")
            # print(key_split)

            # Colocando a API Key no usuário
            # !TODO Verificar se é melhor inserir apenas o prefixo, por motivos de segurança
            # ManageAPIKey.objects.filter(name=username).update(key=generated_key)
            # Testando a biblioteca de logging
            # logging.debug("DEU CERTO MEU PATRÃO")

            # Redireciona para a página inicial, caso dê certo a criação do login

        # Envia um dicionário com o campo não preenchido e o erro relacionado
        # Dá um LOG de erro
        # logging.error(serializer.errors)
        #
        # Coloquei um dicionário com a chave errors para ficar mais legível no html
        # return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Cadastro utilizando Django Templates (Não está sendo utilizado)
def cadastrar(request):
    context = {}
    if request.method == "POST":
        form = CadastroForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        print(form)

        try:
            new_user = User.objects.create_user(**form.cleaned_data)
            print(new_user)
            login(request, user=new_user)

        except IntegrityError:
            form.add_error(error=IntegrityError, field=form.username)
            print("Usuário já existente!!")

        except MultipleObjectsReturned:
            print("MultipleObjectsReturned")
        except TypeError:
            print("Erro de Tipo!")

        return redirect("/")
        # new_user = User.objects.create_user(request.POST)
        # context = {'new_user': new_user}
    return render(request, "cadastro/cadastro.html", context)


# Pesquisa utilizando Django Templates (Não está sendo utilizado)
def pesquisar_vagas(request):
    context = {}
    # context['vagas'] = vagas
    if request.method == "GET":
        print(request.GET)
        vagas = Vagas.objects.get(nome__contains=request.GET['pesquisa'[0]])
        print(vagas)
        context = {'vagas': vagas}
    # response = "Tela de pesquisa de vagas"
    return render(request, context)
