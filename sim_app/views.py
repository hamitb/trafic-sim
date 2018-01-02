from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'form_data': request.POST,
    }

    return render(request, 'sim_app/index.html', context)