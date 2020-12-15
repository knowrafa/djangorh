from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import *
from django.http import HttpResponse, Http404
from django.urls import reverse
from .forms import CadastroForm
from .models import Vagas


def index(request):
    response = "Página de index"
    return HttpResponse(response)


def cadastrar(request):
    # response = "Tela de cadastro"
    context = {}
    form = CadastroForm
    if request.method=="POST":
        form = CadastroForm(request.POST)
        print(request.POST)
        print(form.is_valid())

        try:
            new_user, created = User.objects.create_user(**form.cleaned_data)
            if created:
                new_user.save()
                login(request, user=new_user)
            print(created)
        except IntegrityError:
            print("Usuário já existente!!")
        except MultipleObjectsReturned:
            print("MultipleObjectsReturned")

        return redirect("/")
        # new_user = User.objects.create_user(request.POST)
        # context = {'new_user': new_user}
    return render(request, "cadastro/cadastro.html", context)


def pesquisarvagas(request):
    context = {}
    # context['vagas'] = vagas
    if request.method=="GET":
        print(request.GET)
        vagas =  Vagas.objects.get(nome__contains=request.GET['pesquisa'[0]])
        print(vagas)
    response = "Tela de pesquisa de vagas"
    context ={'vagas': vagas}
    return render(request, context)
