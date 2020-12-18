from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import *
from django.http import HttpResponse
from .forms import CadastroForm
from .models import Vagas
from .serializers import CadastroSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

def index(request):
    response = "Página de index"
    return HttpResponse(response)


class CadastrarUsuario(APIView):
    """
        Lista todas as vagas, utilizando APIView
    """
    #permission_classes = [IsAuthenticatedOrReadOnly] #Se estiver Autenticado pode realizar POST, se não pode apenas realizar GET
    #permission_classes = [IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cadastro/cadastro.html'
    # @login_required DOESNT WORK HERE!!

    def get(self, request, format=None):

        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")
        return Response()

    def post(self, request, format=None):
        serializer = CadastroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("É VÁLIDO")
            print(serializer)
            # print(**serializer)
            ndict = {'serializer': serializer.data}
            print(ndict)
            return Response({'user':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
