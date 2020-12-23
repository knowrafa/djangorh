from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from cadastro.serializers import VagaSerializer, UserSerializer
from cadastro.models import Vagas
from rest_framework import mixins
import requests
import random
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey

# Rest import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics


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


class ApiVagasList(APIView):
    permission_classes = [HasAPIKey] # Rest API Key



    def get(self, request, format=None):

        # Verifica se o usuário está autenticado
        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")

        try:
            pesquisa = request.GET['p']
            vagas = Vagas.objects.filter(nome__contains=pesquisa)

            movie_search = pesquisa
        except:
            movie_search = 'arrival'
            vagas = Vagas.objects.all()

        payload = {"apikey": "53aefdae", "t": movie_search}
        movie_related = requests.get("http://www.omdbapi.com/", params=payload)
        print(movie_related.json())
        serializer = VagaSerializer(vagas, many=True)

        movie = movie_related.json()
        if movie['Response']:
            pass
        return Response({'vagas': serializer.data, 'movie': {'title': movie['Title'], 'director': movie['Director']}})


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

## LOCAL PÚBLICO PARA A PESQUISA DE VAGAS ##
class VagasList(APIView):
    """
        Lista todas as vagas, utilizando APIView
    """
    #permission_classes = [IsAuthenticatedOrReadOnly] #Se estiver Autenticado pode realizar POST, se não pode apenas realizar GET
    #permission_classes = [IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vagas.html'
    # @login_required DOESNT WORK HERE!!

    def get(self, request, format=None):

        # Verifica se o usuário está autenticado
        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")

        #print(request.GET.getlist())

        # Note: verificar se existe mais de um argumento no GET

        if request.GET['p']:
            pesquisa = request.GET['p']
            movie_search = pesquisa
            vagas = Vagas.objects.filter(nome__contains=pesquisa)
        else:
            movie_search = 'arrival'
            vagas = Vagas.objects.all()

        '''
        try:
            pesquisa = request.GET.getlist('pesquisa')
            print(request.GET)
            pesquisa = pesquisa[0]
            vagas = Vagas.objects.filter(nome__contains=pesquisa)

            movie_search = pesquisa
        except:
            movie_search = 'arrival'
            vagas = Vagas.objects.all()
        '''

        payload = {"apikey": "53aefdae", "t": movie_search}
        movie_related = requests.get("http://www.omdbapi.com/", params=payload)
        #print(movie_related.json())
        serializer = VagaSerializer(vagas, many=True)

        movie = movie_related.json()
        if movie['Response']:
            pass

        return Response({'vagas': serializer.data, 'movie': {'title': movie['Title'], 'director': movie['Director']}})

    def post(self, request, format=None):
        serializer = VagaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
def ver_vagas(request):
    context = {}
    context['vagas'] = Vagas.objects.all()
    if request.method=="GET":
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

    def get(self, request):
        return Response()

    def post(self, request):
        return Response()


def homepage(request):
    context={"name":request.user.username}
    return HttpResponse("AQUI É SUA HOMEPAGE " + context["name"])


class LogoutUser(APIView):
    """
        Homepage do usuário
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


# UTILIZANDO DJANGO TEMPLATE
@login_required
def logout_page(request):
    #Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')