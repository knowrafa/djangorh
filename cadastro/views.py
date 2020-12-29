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

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cadastro/cadastro.html'
    # @login_required DOESNT WORK HERE!!

    @staticmethod
    def get(request):

        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")
        return Response()

    @staticmethod
    def post(request):
        serializer = CadastroSerializer(data=request.data)

        # Testar se o serializer fica válido com mais informações do que o necessário
        if serializer.is_valid():

            # Verifica se o create funciona (retorna True ou False - Método sobrescrito)
            if serializer.create(validated_data=serializer.data):

                # Testando a biblioteca de logging
                logging.debug("DEU CERTO MEU PATRÃO")

                # Redireciona para a página inicial, caso dê certo a criação do login
                return HttpResponseRedirect(redirect_to='/')

        # Envia um dicionário com o campo não preenchido e o erro relacionado
        # Dá um LOG de erro
        logging.error(serializer.errors)

        # Coloquei um dicionário com a chave errors para ficar mais legível no html
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def cadastrar(request):
    # response = "Tela de cadastro"
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


def pesquisarvagas(request):
    context = {}
    # context['vagas'] = vagas
    if request.method == "GET":
        print(request.GET)
        vagas = Vagas.objects.get(nome__contains=request.GET['pesquisa'[0]])
        print(vagas)
        context = {'vagas': vagas}
    # response = "Tela de pesquisa de vagas"
    return render(request, context)
