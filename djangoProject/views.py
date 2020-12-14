from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from cadastro.models import Vagas

def main_page(request):
    context = {'user': request.user}
    return render_to_response('index.html', context)


# @login_required() - Comentado pois é uma área pública de acesso
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
            context['vagas'] = vagas
    return render(request, "vagas.html", context)


@login_required
def second_page(request):
    return HttpResponse("ola")

@login_required
def homepage(request):
    context={"name":request.user.username}
    return HttpResponse("AQUI É SUA HOMEPAGE " + context["name"])

@login_required
def logout_page(request):
    #Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')