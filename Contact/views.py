from django.http import JsonResponse
from Contact.models import Person
import json

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
    return JsonResponse({'status': status})

def edit_person(request):
    #restricting in-appropriate methods, pet project so fine.
    #in prod, people can find loopholes to attack the site
    if request.method != 'PATCH':
        return JsonResponse({'status': f'Wrong http used - ({request.method})'})
    edited = []
    data = json.loads(request.body)#reading PATCH data
    adr = data.get('aadhar')
    if adr is None:
        return JsonResponse({"status": "Aadhar is missing, mandatory to edit"})
    nam = data.get('name')
    d = data.get('dob')
    em = data.get('email')
    mb = data.get('mobile')
    dp = data.get('dp_pic')
    editable = nam or d or em or mb or dp
    if not editable:
        return JsonResponse({"status":"Update at least one field"})
    try:
        cur = Person.objects.get(aadhar=adr)
    except:
        return JsonResponse({"status": f"Invalid Aadhar({adr}) given"})
    else:
        cols = (
            ('name', nam), ('dob', d), ('email', em),
            ('mobile', mb), ('dp_pic', dp),
        )
        for col_name, col_val in cols:
            if col_val:
                edited.append(col_name)
                exec(f"cur.{col_name} = '{col_val}'")
        cur.save()
    edited = ", ".join(edited)
    return JsonResponse({"status": f"Edited {edited} for {adr}"})

def read_person(request):
    if request.method == 'GET':
        adr = request.GET.get('aadhar')
        try:
            cur = Person.objects.get(aadhar=adr)
        except:
            return JsonResponse({'status': f"No Such Contact({adr})"})
        else:
            res = str(cur.get_details())
            return JsonResponse({'status': res})
    else:
        #pet project :)
        return JsonResponse({'status': f'Wrong http used - ({request.method})'})
    
def delete_person(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        adr = data.get('aadhar')
        try:
            cur = Person.objects.get(aadhar=adr)
            cur.delete()
        except:
            return JsonResponse({'status': f"No Such Contact({adr})"})
        else:
            return JsonResponse({'status': f"Contact({adr}) deleted"})
    else:
        #pet project :)
        return JsonResponse({'status': f'Wrong http used - ({request.method})'})
