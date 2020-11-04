from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import StretchingData, WaterData
import json

# Create your views here.

def signup(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            username = req_data['username']
            email = req_data['email']
            password = req_data['password']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponse(status=400)
        User.objects.create_user(username, email, password)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)

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

def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)

