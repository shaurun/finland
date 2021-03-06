import json

from bson.json_util import dumps
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from FinLand.mongo import MongoDBClient

client = MongoDBClient('mongodb://heroku_4nzjwz0z:dcvtdbro5ppqqahpdrc8m83lcl@ds131902.mlab.com/heroku_4nzjwz0z', 31902)
client.connect('heroku_4nzjwz0z')


def index(request):
    return render(request, "index.html");


def returnMatrixData(request):
    return_matrix = client.find_document("return_matrices", {"user": auth.get_user(request).id})
    return JsonResponse(json.loads(dumps(return_matrix)))

def returnMatrix(request):
    if (request.POST):
        return_matrix = request.POST.get('return_matrix');
        obj = json.loads(return_matrix);
        del obj["_id"]
        client.update_document("return_matrices", {"user":auth.get_user(request).id}, { '$set':  obj })
        return JsonResponse(json.loads('{"status": "ok"}'))
    else:
        if (request.META.get('CONTENT_TYPE') == 'application/json'):
            return returnMatrixData(request);
        return render(request, "returnMatrix.html");

def moneyFlow(request):
    if (request.POST):
        money_flow = '{"years": [ ' + request.POST.get('money_flow') + ']}';
        client.update_document("money_flow", {"user":auth.get_user(request).id}, { '$set':  json.loads(money_flow) })
    else:
        money_flow = client.find_document("money_flow", {"user": auth.get_user(request).id})
        if (money_flow is None):
            createMoneyFlow(auth.get_user(request))
            money_flow = client.find_document("money_flow", {"user": auth.get_user(request).id})
        context = {"money_flow" : money_flow}
        return render(request, "moneyFlow.html", context);

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
                client.insert_document("return_matrices", {
                    "user":user.id,
                    "present_value": "500,000",
                    "years": 15,
                    "actual_contributions": "1,000,000"})
                createMoneyFlow(user);

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

def createMoneyFlow(user):
    client.insert_document("money_flow", {
        "user": user.id,
        "years": [
            {"year" : 2018,
                "categories": [
                    {"name": "Custom 1", "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                    {"name": "Custom 2", "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                    {"name": "Bonus - Cash", "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                    {"name": "Bonus - Newport", "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]}]
            },
            {"year" : 2019,
                "categories": [{"name": "Custom 1",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Custom 2",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Bonus - Cash",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Bonus - Newport",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]}]
            },
            {"year" : 2020,
                "categories": [{"name": "Custom 1",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Custom 2",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Bonus - Cash",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]},
                               {"name": "Bonus - Newport",
                                "values": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]}]
             }]
    })
