import random

import requests


# Create your views here.
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey

from cadastro.models import Vagas
from cadastro.serializers import VagaSerializer


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
            # movie_search = pesquisa]
            # variable__contains -> case sensitive
            # variable__icontains -> case insensitive
            vagas = Vagas.objects.filter(nome__icontains=pesquisa)
            # vagas = Vagas.objects.filter(nome__contains=pesquisa)
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

        # Serializar pra quê?
        # serializer = VagaSerializer(vagas, many=True)

#        # payload = {"apikey": "53aefdae", "t": movies[random.randint(0, len(movies) - 1)]}
#        # movie_related = requests.get("http://www.omdbapi.com/", params=payload)

        # Inicializando dicionário com um espaço de vagas
        r_dict = {'vagas': []}
        for vaga in vagas:

            # Criando payload e fazendo requisição na api omdb
            payload = {"apikey": "53aefdae", "t": movies[random.randint(0, len(movies) - 1)]}
            movie_related = requests.get("http://www.omdbapi.com/", params=payload)
            movie = movie_related.json()

            # Serializando vaga para poder utilizar o .data (!TODO verificar se a vaga crua tem .data)
            serialize_vaga = VagaSerializer(vaga)

            # Alimentando o dicionário de vagas com um filme aleatório para cada uma
            # - Desconstruindo o dict serialize_vaga.data
            # - Adicionando campos novos (title e director)
            # - Reconstruindo o dicionário
            # - Guardando na lista de vagas com 'title' e 'director'
            r_dict['vagas'].append({**serialize_vaga.data, 'title': movie['Title'], 'director': movie['Director']})
        # print(movie_related.json())

        # movie = movie_related.json()
        # if movie['Response']:
        #    pass

        # return Response({'vagas': serializer.data, 'movie': {'title': movie['Title'], 'director': movie['Director']}})
        return Response(r_dict)

    @staticmethod
    def post(request):
        serializer = VagaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiVagasList(APIView):
    """
    API para listar as vagas cadastradas na aplicação
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
                APIKey.objects.get_from_key(api_key)
            except APIKey.DoesNotExist:
                # Se der merda já sabe
                payload['response'] = False
                payload['error'] = 'Invalid API Key'
                get_status = status.HTTP_418_IM_A_TEAPOT
            else:
                # Executa quando o try não tem problemas
                vagas = Vagas.objects.all()
                payload['response'] = True

                # Serializa todos as vagas e guarda na lista de vagas
                serializer = VagaSerializer(vagas, many=True)
                payload['vagas'] = serializer.data

                # Nome na criação da API Key
                # payload['user'] = api_key.name
                get_status = status.HTTP_200_OK
        else:
            payload['response'] = False
            payload['error'] = 'No API Key provided'
            get_status = status.HTTP_403_FORBIDDEN

        return Response(payload, status=get_status)
