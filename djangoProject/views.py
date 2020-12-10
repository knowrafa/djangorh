from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from cadastro.models import Vagas

def main_page(request):
    return render_to_response('index.html')


@login_required()
def ver_vagas(request):
    context = {'full_name': request.user.username}
    Vagas.objects.all()
    return render_to_response('vagas.html', context)


@login_required
def second_page(request):
    return HttpResponse("ola")

def logout_page(request):
    #Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')