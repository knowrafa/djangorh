# Django imports
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render

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


class ApiVagasList(APIView):
    """
    Comando para criar uma API Key (Colocar na hora do cadastro)
    api_key, key = APIKey.objects.create_key(name="my-remote-service")
    """
    @staticmethod
    def get(request):
        # Verifica se o usuário está autenticado
        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")

        payload = {}
        # O parâmetro key pega a payload do get
        api_key = request.GET.get('apikey')
        if api_key:
            # Se existir API Key, então verificar
            try:
                # Se de todos os objetos API Key tiver o usuário, então é válido
                # Em outro caso cai no except
                api_key = APIKey.objects.get_from_key(api_key)
            except APIKey.DoesNotExist:
                # Se der merda já sabe
                payload['response'] = False
                payload['error'] = 'Invalid API Key'
                get_status = status.HTTP_418_IM_A_TEAPOT
            else:
                # Executa quando o try não tem problemas
                vagas = Vagas.objects.all()
                payload['response'] = True

                # Serializa todos as vagas
                serializer = VagaSerializer(vagas, many=True)
                payload['vagas'] = serializer.data

                # Nome na criação da API Key
                payload['user'] = api_key.name
                get_status = status.HTTP_200_OK
        else:
            payload['response'] = False
            payload['error'] = 'No API Key provided'
            get_status = status.HTTP_403_FORBIDDEN

        return Response(payload, status=get_status)


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


# LOCAL PÚBLICO PARA A PESQUISA DE VAGAS #
class VagasList(APIView):
    """
        Lista todas as vagas, utilizando APIView
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # Se estiver Autenticado pode realizar POST, se não pode apenas realizar GET
    # permission_classes = [IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vagas.html'

    # @login_required DOESNT WORK HERE!!

    @staticmethod
    def get(request):

        # Verifica se o usuário está autenticado
        # if not request.user.is_authenticated:
        #    return HttpResponseRedirect("/login?next=/vagas/")

        # print(request.GET.getlist())

        # Note: verificar se existe mais de um argumento no GET

        movies = [
            'Arrival',
            'Superman',
            'Die Hard',
            'Black',
            'Earth',
            'Python',
            'Devil',
            'Justice League',
            'Avengers',
            'Infinity War',

        ]

        if request.GET.getlist('p'):
            pesquisa = request.GET['p']
            # movie_search = pesquisa
            vagas = Vagas.objects.filter(nome__contains=pesquisa)
        else:
            # movie_search = 'arrival'
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
        # for vaga in vagas:
        #    vaga['movie_related'] = movies[random.randint(0, len(movies)-1)]

        payload = {"apikey": "53aefdae", "t": movies[random.randint(0, len(movies) - 1)]}
        movie_related = requests.get("http://www.omdbapi.com/", params=payload)
        # print(movie_related.json())
        serializer = VagaSerializer(vagas, many=True)

        movie = movie_related.json()
        if movie['Response']:
            pass

        return Response({'vagas': serializer.data, 'movie': {'title': movie['Title'], 'director': movie['Director']}})

    @staticmethod
    def post(request):
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
