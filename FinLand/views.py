from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from pymongo.errors import OperationFailure

from FinLand.models import Section
from FinLand.mongo import MongoDBClient

#client = MongoDBClient('localhost', 27017)
client = MongoDBClient('mongodb://heroku_4nzjwz0z:dcvtdbro5ppqqahpdrc8m83lcl@ds131902.mlab.com/heroku_4nzjwz0z', 31902)
#client.connect('finlandDB')
client.connect('heroku_4nzjwz0z')

def index(request):
    return render(request, "index.html");

def returnMatrix(request):

    user = client.find_document("users", {"name": "James"})

    #client.insert_document('users', {"name": "James", "password": "pass"})
    #user = client.find_document("users", {"name": "James"})
    #client.insert_document("return_matrices", {"user":user['_id'], "present_value": "500,000", "years": 15, "actual_contributions": "1,000,000"})

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

def register(request):
    args = {};
    args.update(csrf(request));
    args['form'] = UserCreationForm();
    if (request.POST):
        new_user_form = UserCreationForm(request.POST);
        if (new_user_form.is_valid()):
            new_user_form.save();
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2']);
            auth.login(request, new_user);
            return redirect("/");
        else:
            args['form'] = new_user_form;
    return render(request, "register.html", args);

