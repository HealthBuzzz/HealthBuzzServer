from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import StretchingData, WaterData
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            username = req_data['username']
            email = req_data['email']
            password = req_data['password']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponse(status=400)
        User.objects.create_user(username=username, email=email, password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            email = req_data['email']
            password = req_data['password']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponse(status=400)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def waterdata(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        waterdata_list = []
        for waterdata in WaterData.objects.all().values():
            if waterdata['user_id'] == request.user.id:
                waterdata_list.append({
                    'user': waterdata['user_id'],
                    'year': waterdata['year'],
                    'month': waterdata['month'],
                    'day': waterdata['day'],
                    'amount': waterdata['amount'],
                })
        return JsonResponse(waterdata_list, status=200, safe=False)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        try:
            req_data = json.loads(request.body.decode())
            year = req_data['year']
            month = req_data['month']
            day = req_data['day']
            amount = req_data['amount']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponse(status=400)
        waterdata = WaterData(user_id=request.user.id, year=year, month=month,
                day=day, amount=amount)
        waterdata.save()
        response_dict = {'id': waterdata.id, 'year': waterdata.year, 'month':
                waterdata.month, 'day': waterdata.day, 'amount':
                waterdata.amount}
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def stretchingdata(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        stretchingdata_list = []
        for stretchingdata in StretchingData.objects.all().values():
            if stretchingdata['user_id'] == request.user.id:
                stretchingdata_list.append({
                    'user': stretchingdata['user_id'],
                    'year': stretchingdata['year'],
                    'month': stretchingdata['month'],
                    'day': stretchingdata['day'],
                    'amount': stretchingdata['amount'],
                })
        return JsonResponse(stretchingdata_list, status=200, safe=False)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        try:
            req_data = json.loads(request.body.decode())
            year = req_data['year']
            month = req_data['month']
            day = req_data['day']
            amount = req_data['amount']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponse(status=400)
        stretchingdata = StretchingData(user_id=request.user.id, year=year, month=month,
                day=day, amount=amount)
        stretchingdata.save()
        response_dict = {'id': stretchingdata.id, 'year': stretchingdata.year, 'month':
                stretchingdata.month, 'day': stretchingdata.day, 'amount':
                stretchingdata.amount}
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponse(status=405)

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])
