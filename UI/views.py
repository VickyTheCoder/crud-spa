from django.shortcuts import render, HttpResponse

# Create your views here.
def home_page(request):
    if request.method == 'GET':
        return render(request=request, 
                      template_name='index.html')
    return HttpResponse("Wrong Request")