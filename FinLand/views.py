from django.shortcuts import render

from FinLand.models import Section
from FinLand.mongo import MongoDBClient

client = MongoDBClient('localhost', 27017)
client.connect('finlandDB')

def index(request):
    return render(request, "index.html");

def returnMatrix(request):
    user = client.find_document("users", {"name": "James"})
    if (request.POST):
        years = request.POST.get('years', '');
        present_value = request.POST.get('present_value', 18);
        actual_contributions = request.POST.get('actual_contributions', '');
        obj = {
            "present_value": present_value,
            "years": int(years),
            "actual_contributions": actual_contributions
        };
        client.update_document("return_matrices", {"user":user['_id']}, { '$set':  obj })
    else:
        return_matrix = client.find_document("return_matrices" , {"user":user['_id']})
        context = {
            "return_matrix" : return_matrix
            #"present_value": "500,000",
            #"years": 15,
            #"actual_contributions": "1,000,000"
        }
        return render(request, "returnMatrix.html", context);

def moneyFlow(request):
    return render(request, "moneyFlow.html");

def dbTest(request):
    #client = MongoDBClient('localhost', 27017)
    #client.connect('finlandDB')
    #client.insert_document('james', {"user": "James", "sections": ["custom1", "custom2"]});
    for item in client.find_all('posts', {"user": "James"}):
        print(item)
    sections = Section.objects.all();
    context = {
        'sections': sections
    }
    return render(request, "dbtest.html", context);

