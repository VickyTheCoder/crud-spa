from django.shortcuts import render, HttpResponse
from Contact.forms import PersonForm

# Create your views here.
def home_page(request):
    if request.method == 'GET':
        return render(request=request, 
                      template_name='index.html',
                      context={'add_form': PersonForm})
    return HttpResponse("Wrong Request")