from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.


def index(request):
    response = "Página de index"
    return HttpResponse(response)


def error404(request):
    Http404("Error")


def cadastrar(request):
    # response = "Tela de cadastro"
    context = {"ola_mundo": "Olá mundo do html!"}
    return render(request, "cadastro/cadastro.html", context)


def pesquisarvagas(request):
    response = "Tela de pesquisa de vagas"
    return HttpResponse(response)
