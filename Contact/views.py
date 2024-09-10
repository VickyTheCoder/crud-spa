from django.http import JsonResponse
from Contact.models import Person

# Create your views here.
def add_person(request):
    adr = request.POST.get('aadhar')
    nam = request.POST.get('name')
    d = request.POST.get('dob')
    em = request.POST.get('email')
    mb = request.POST.get('mobile')
    dp = request.POST.get('dp_pic')
    try:
        #this should throw error if the aadhar is already there
        #in the DB, probably duplicate
        Person.objects.get(aadhar=adr)
    except:
        row = Person(aadhar=adr, name=nam, dob=d, email=em, mobile=mb, dp_pic=dp)
        row.save()
        try:
            #should not raise exception
            #if the above "row.save()" worked fine
            Person.objects.get(aadhar=adr)
        except:
            #this means the save failed!!
            status = "Insert Failed"
        else:
            status = "Inserted"        
    else:
        status = "Already Existing data"
    return JsonResponse({'status': statusq})

