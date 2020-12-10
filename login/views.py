from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def login(request):
    """
     If users are authenticated, direct them to the main page. Otherwise, take
     them to the login page.
     """
    context = {'full_name': request.user.username}
    return render_to_response('login/login.html', context)

@login_required()
def mostrarvagas(request):
    return HttpResponse("Olá mundo!")
