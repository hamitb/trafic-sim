from django.shortcuts import render

# Create your views here.
def index(request):
    if 'post_message' not in request.session:
        request.session['post_message'] = request.get_host()

    context = {
        'form_data': request.POST,
        'post_message': request.session['post_message'],
    }

    return render(request, 'sim_app/index.html', context)