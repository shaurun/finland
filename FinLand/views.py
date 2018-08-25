from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from FinLand.mongo import MongoDBClient

client = MongoDBClient('mongodb://heroku_4nzjwz0z:dcvtdbro5ppqqahpdrc8m83lcl@ds131902.mlab.com/heroku_4nzjwz0z', 31902)
client.connect('heroku_4nzjwz0z')

def index(request):
    return render(request, "index.html");

def returnMatrix(request):
    if (request.POST):
        years = request.POST.get('years', '');
        present_value = request.POST.get('present_value', 18);
        actual_contributions = request.POST.get('actual_contributions', '');
        obj = {
            "present_value": present_value,
            "years": int(years),
            "actual_contributions": actual_contributions
        };
        client.update_document("return_matrices", {"user":auth.get_user(request).id}, { '$set':  obj })
    else:
        return_matrix = client.find_document("return_matrices" , {"user":auth.get_user(request).id})
        context = {
            "return_matrix" : return_matrix
            #"present_value": "500,000",
            #"years": 15,
            #"actual_contributions": "1,000,000"
        }
        return render(request, "returnMatrix.html", context);

def moneyFlow(request):
    return render(request, "moneyFlow.html");

def logout(request):
    auth.logout(request);
    return redirect("/");

def login(request):
    args = {};
    args.update(csrf(request));
    if (request.POST):
        username = request.POST.get('username', '');
        password = request.POST.get('password', '');
        email = request.POST.get('email', '');
        args['username'] = username;
        args['password'] = password;
        args['email'] = email;
        if (username == '' or password == ''):
            args['login_error'] = "Заполните имя пользователя и пароль";
            return render(request, "index.html", args);
        else:
            if (request.POST.get('action') == "Register"):
                user = User.objects.create_user(username, email, password)
            elif (request.POST.get('action') == "Login"):
                user = auth.authenticate(username=username, password=password);

            if (user is not None):
                auth.login(request, user);
                return redirect("/");
            else:
                args['login_error'] = "Пользователь не найден.";
                return render(request, "register.html", args);
    else:
        return render(request, "register.html")

