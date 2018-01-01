from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'message': 'Hello'
    }
    return render(request, 'sim_app/index.html', context)