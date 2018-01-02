from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from util.server import rpc_service

# Create your views here.
def index(request):
    context = {
        'session_id': request.session.session_key,
    }
    rpc_service(request.session.session_key, quick_start=True)
    return render(request, 'sim_app/index.html', context)

def settings(request, component):

    return HttpResponseRedirect(reverse('sim_app:index'))
