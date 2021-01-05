# Django imports
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
# from cadastro.models import ManageAPIKey
# Cadastro imports
from cadastro.serializers import VagaSerializer
from cadastro.models import Vagas

# Another Libs
import requests
import random

# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework_api_key.permissions import HasAPIKey

# Rest Framework imports
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_api_key.models import APIKey


def main_page(request):
    context = {'user': request.user}
    return render_to_response('index.html', context)


# @csrf_exempt DECORATOR - Caso eu não queira exigir o crsf
# GET (LIST, return a list of dicts) POST


class VagasListGeneric(generics.ListCreateAPIView):
    queryset = Vagas.objects.all()
    serializer_class = VagaSerializer


# GET (retrieve - A SINGLE DICT, requires ID) PUT DELETE
class VagasDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vagas.objects.all()
    serializer_class = VagaSerializer


class VagasListMixin(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
        Lista todas as vagas, utilizando APIView
    """
    # template_name = "vagas.html"

    queryset = Vagas.objects.all()
    serializer_class = VagaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


'''
@api_view(['GET', 'POST'])
def ver_vagas_rest(request):
    """
    Listar todas as vagas ou criar uma nova vaga
    """
    if request.method == 'GET':
        vagas = Vagas.objects.all()
        serializer = VagaSerializer(vagas, many=True)
        return Response(template_name="vagas.html",  data=serializer.data)

    elif request.method == 'POST':
        serializer = VagaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


# @login_required() # UTILIZANDO DJANGO TEMPLATE
# Utilizando Django rest, não mais template Django
def ver_vagas(request):
    context = {'vagas': Vagas.objects.all()}
    if request.method == "GET":
        if request.GET:
            print(request.GET)
            pesquisa = request.GET.getlist('pesquisa')
            print(pesquisa)
            pesquisa = pesquisa[0]
            vagas = Vagas.objects.filter(nome__contains=pesquisa)
            print(vagas)
            context['vagas'] = vagas
    return render(request, "vagas.html", context)


# Utilizando DJANGO TEMPLATE
# Teste com o decorator @login_required
@login_required
def second_page(request):
    return HttpResponse("ola")


# UTILIZANDO DJANGO TEMPLATE PARA AUTENTICAÇÃO

# API REST PARA A VIEW DA PÁGINA INICIAL DO USUARIO
class HomePageUserView(APIView):
    """
        Homepage do usuário
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    @staticmethod
    def get(request):
        return Response()

    @staticmethod
    def post(request):
        return Response()


# Django Template
def homepage(request):
    context = {"name": request.user.username}
    return HttpResponse("AQUI É SUA HOMEPAGE " + context["name"])


class LogoutUser(APIView):
    """
        Homepage do usuário, utilizando APIView do REST
    """
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect('/')


# UTILIZANDO DJANGO TEMPLATE
# Deixando como exemplo (Não está sendo utilizado)
@login_required
def logout_page(request):
    # Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')
