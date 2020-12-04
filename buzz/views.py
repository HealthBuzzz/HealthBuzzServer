from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import StretchingData, WaterData, Profile, DailyStretching, DailyWater
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
import json
from json.decoder import JSONDecodeError
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
        new_user = User.objects.create_user(username=username, email=email, password=password)
        user_info = {
            'id': new_user.id,
            'name': new_user.username,
        }
        profile = Profile(user=new_user)
        profile.save()
        return JsonResponse(user_info, status=201) 
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
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist as e:
            return HttpResponse(status=401)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            user_info = {
                'id': user.id,
                'name': user.username,
            }
            return JsonResponse(user_info, status=200)
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
        response_dict = {
            'id': waterdata.id, 
            'year': waterdata.year, 
            'month': waterdata.month, 
            'day': waterdata.day, 
            'amount': waterdata.amount
            }
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
        response_dict = {'id': stretchingdata.id, 
                         'year': stretchingdata.year, 
                         'month': stretchingdata.month, 
                         'day': stretchingdata.day, 
                         'amount': stretchingdata.amount,
                         }
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponse(status=405)
    
@csrf_exempt
def today(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        ranking_stretch = calculate_ranking_stretch(request.user)
        ranking_water = calculate_ranking_water(request.user)
        profile = request.user.profile
        profile.today_ranking = ranking
        profile.save()
        
        response = {
            'today_stretching_count': profile.today_stretching_count,
            'today_water_count': profile.today_water_count,
            'today_ranking_stretch': profile.today_ranking_stretch,
            'today_ranking_water': profile.today_ranking_water,
        }
        return JsonResponse(response, status=200)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def today_refresh(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        new = StretchingData(
            user=request.user,
            year=datetime.today().year,        # 현재 연도 가져오기
            month=datetime.today().month,
            day=datetime.today().day,
            amount=request.user.profile.today_stretching_count,
        )
        new.save()
        request.user.profile.today_stretching_count = 0
        request.user.profile.today_water_count = 0
        request.user.profile.today_ranking_stretch = 100
        request.user.profile.today_ranking_water = 100
        request.user.profile.save()

        response = {
            'today_stretching_count': profile.today_stretching_count,
            'today_water_count': profile.today_water_count,
            'today_ranking_stretch': profile.today_ranking_stretch,
            'today_ranking_water': profile.today_ranking_water,
        }
        return JsonResponse(response, status=200)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def today_stretching(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        response = list(DailyStretching.objects \
                        .filter(user_id=request.user.id).values('hour','minute'))
        return JsonResponse(response, status=200, safe=False)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        req_data = json.loads(request.body.decode())
        profile = request.user.profile
        daily_stretching = DailyStretching(user=request.user,
                                          hour=req_data['hour'],
                                          minute=req_data['minute'])
        daily_stretching.save()
        profile.today_stretching_count = profile.today_stretching_count + 1

        ranking = calculate_ranking_stretch(request.user)
        profile.today_ranking_stretch = ranking

        profile.save()
        response = {
            'today_stretching_count': profile.today_stretching_count,
            'today_water_count': profile.today_water_count,
            'today_ranking_stretch': profile.today_ranking_stretch,
            'today_ranking_water': profile.today_ranking_water,
        }
        return JsonResponse(response, status=201)

@csrf_exempt
def today_water(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        response = list(DailyWater.objects \
                        .filter(user_id=request.user.id).values('hour','minute'))
        return JsonResponse(response, status=200, safe=False)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        req_data = json.loads(request.body.decode())
        profile = request.user.profile
        #daily_water = DailyWater(user=request.user,
        #                                  hour=req_data['hour'],
        #                                  minute=req_data['minute'],
        #                                  amount=req_data['amount'])
        #daily_water.save()
        profile.today_water_count = req_data.amount

        ranking = calculate_ranking_water(request.user)
        profile.today_ranking_water = ranking

        profile.save()
        response = {
            'today_stretching_count': profile.today_stretching_count,
            'today_water_count': profile.today_water_count,
            'today_ranking_stretch': profile.today_ranking_stretch,
            'today_ranking_water': profile.today_ranking_water,
        }
        return JsonResponse(response, status=201)

def calculate_ranking_stretch(user):
    id_and_point_list = []
    for profile in Profile.objects.values():
        point = profile['today_stretching_count']
        id_and_point_list.append((profile['user_id'], point))
    sorted(id_and_point_list, key=lambda id_and_point: id_and_point[1])
    for i, id_and_point in enumerate(id_and_point_list):
        if id_and_point[0] == user.id:
            return int(((i+1) / len(id_and_point_list))*100)
    # No profile that includes the user
    return -1

def calculate_ranking_water(user):
    id_and_point_list = []
    for profile in Profile.objects.values():
        point = profile['today_water_count']
        id_and_point_list.append((profile['user_id'], point))
    sorted(id_and_point_list, key=lambda id_and_point: id_and_point[1])
    for i, id_and_point in enumerate(id_and_point_list):
        if id_and_point[0] == user.id:
            return int(((i+1) / len(id_and_point_list))*100)
    # No profile that includes the user
    return -1

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

