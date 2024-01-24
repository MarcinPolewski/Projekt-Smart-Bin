from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from TrashApp.models import *
from TrashApp.serializers import *
from rest_framework.viewsets import ModelViewSet
from django.forms.models import model_to_dict
import json
import copy
from datetime import datetime
import urllib.parse
from django.core.mail import send_mail
# Create your views here.

def send_info(bin_id, who_did):
    users = TblUzytkownicyKonfig.objects.all()
    users_serializer = TblUzytkownicyKonfigSerializer(users, many=True)
    bin = TblKoszeKonfiguracyjna.objects.get(id_bin=bin_id)
    bin_serializer = TblKoszeKonfiguracyjnaSerializer(bin)
    bin_name = bin_serializer.data['bin_name']
    our_mail = 'trasherspw@gmail.com'
    recipents_list = []
    for user in users_serializer.data:
        if user['id_user'] == who_did:
            who_did_name= user['user_name']
    content = f'The trash in {bin_name} has been taken out by {who_did_name}.'
    for user in users_serializer.data:
        print(user['which_bin'])
        mail = user['user_mail']
        recipents_list.append(mail)
        print(content)
        print(mail)
        print(our_mail)
    send_mail("Trash taken out", content, our_mail, recipents_list, fail_silently = False)




@csrf_exempt
def userApi(request, id=0):
    if request.method == "GET":
        user = TblUzytkownicyKonfig.objects.all()
        user_serializer = TblUzytkownicyKonfigSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = TblUzytkownicyKonfigSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = TblUzytkownicyKonfig.objects.get(id_user=user_data["id_user"])
        user_serializer = TblUzytkownicyKonfigSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method == "DELETE":
        user = TblUzytkownicyKonfig.objects.get(id_user=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def binApi(request, id=0):
    if request.method == "GET":
        user = TblKoszeKonfiguracyjna.objects.all()
        user_serializer = TblKoszeKonfiguracyjnaSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = TblKoszeKonfiguracyjnaSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = TblKoszeKonfiguracyjna.objects.get(id_bin=user_data["id_bin"])
        user_serializer = TblKoszeKonfiguracyjnaSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method == "DELETE":
        user = TblKoszeKonfiguracyjna.objects.get(id_bin=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def logsApi(request, id=0):
    if request.method == "GET":
        user = TblBinLogs.objects.all()
        user_serializer = TblBinLogsSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == "POST":
        print(request)
        user_data = request.POST.dict()
        try:
            user_data = JSONParser().parse(request)
        except Exception:
            pass
        current_date = datetime.now()
        date_string = current_date.strftime("%d-%m-%Y %H:%M")
        user_data.update({"date_log": date_string})
        user_serializer = TblBinLogsSerializer(data=user_data)
        new_bin_status = user_data["bin_status"]
        bin = TblKoszeKonfiguracyjna.objects.get(id_bin=user_data["bin_id"])
        bin_serializer = TblKoszeKonfiguracyjnaSerializer(bin)
        bin_data = bin_serializer.data
        bin_data.update({"bin_status": new_bin_status})
        bin_serializer = TblKoszeKonfiguracyjnaSerializer(bin, bin_data)
        if bin_serializer.is_valid():
            bin_serializer.save()
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = TblBinLogs.objects.get(id_log=user_data["id_log"])
        user_serializer = TblBinLogsSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method == "DELETE":
        user = TblBinLogs.objects.get(id_log=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def scheduleApi(request, id=0):
    if request.method == "GET":
        user = TblHarmonogramWyn.objects.all()
        user_serializer = TblHarmonogramWynSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = TblHarmonogramWynSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = TblHarmonogramWyn.objects.get(id_daty=user_data["id_daty"])
        user_serializer = TblHarmonogramWynSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method == "DELETE":
        user = TblHarmonogramWyn.objects.get(id_daty=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def takeoutApi(request, id=0):
    if request.method == "GET":
        takeout = TblWynoszenie.objects.all()
        takeout_serializer = TblWynoszenieSerializer(takeout, many=True)
        return JsonResponse(takeout_serializer.data, safe=False)
    elif request.method == "POST":
        takeout_data = (request.POST).dict()
        try:
            takeout_data = JSONParser().parse(request)
        except Exception:
            # reuquest_without_b = str(request.POST).strip("b'")
            pass
        takeout_serializer = TblWynoszenieSerializer(data=takeout_data)
        current_date = datetime.now()
        date_string = current_date.strftime("%Y-%m-%d %H:%M:%S")
        takeout_data.update({"date": date_string})
        bin = TblKoszeKonfiguracyjna.objects.get(id_bin = 1)
        bin_data = TblKoszeKonfiguracyjnaSerializer(bin).data

        add_points = int(bin_data['adding_points'])
        add_points_user = TblUzytkownicyKonfig.objects.get(
            id_user=takeout_data["who_did"]
        )
        sub_points_user = None
        if (takeout_data.get("who_should")) != (takeout_data.get("who_did")):
            sub_points_user = TblUzytkownicyKonfig.objects.get(
                id_user=takeout_data["who_should"]
            )
            sub_points = int(bin_data['subtrack_points'])
        user_serializer = TblUzytkownicyKonfigSerializer(add_points_user)
        user_data = user_serializer.data
        current_user_points = user_data["points_status"]
        current_user_points += add_points
        user_data.update({"points_status": current_user_points})
        user_serializer_new = TblUzytkownicyKonfigSerializer(
            add_points_user, data=user_data
        )
        if sub_points_user:
            sub_serializer = TblUzytkownicyKonfigSerializer(sub_points_user)
            sub_data = sub_serializer.data
            current_sub_points = sub_data["points_status"]
            current_sub_points += -sub_points
            sub_data.update({"points_status": current_sub_points})
            sub_serializer_new = TblUzytkownicyKonfigSerializer(
                sub_points_user, data=sub_data
            )
            print(sub_data)
            if sub_serializer_new.is_valid():
                sub_serializer_new.save()
        takeout_serializer = TblWynoszenieSerializer(data=takeout_data)
        print(takeout_data)
        send_info(takeout_data['which_bin'], takeout_data['who_did'])
        if takeout_serializer.is_valid():
            takeout_serializer.save()
        if user_serializer_new.is_valid():
            user_serializer_new.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = TblWynoszenie.objects.get(id_empty=user_data["id_empty"])
        user_serializer = TblWynoszenieSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succsefully", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method == "DELETE":
        user = TblWynoszenie.objects.get(id_empty=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


class UserViewSet(ModelViewSet):
    serializer_class = TblUzytkownicyKonfigSerializer
    queryset = TblUzytkownicyKonfig.objects.all()


class BinViewSet(ModelViewSet):
    serializer_class = TblKoszeKonfiguracyjnaSerializer
    queryset = TblKoszeKonfiguracyjna.objects.all()


class LogsViewSet(ModelViewSet):
    serializer_class = TblBinLogsSerializer
    queryset = TblBinLogs.objects.all()


class TakeoutViewSet(ModelViewSet):
    serializer_class = TblWynoszenieSerializer
    queryset = TblWynoszenie.objects.all()


class ScheduleViewSet(ModelViewSet):
    serializer_class = TblHarmonogramWynSerializer
    queryset = TblHarmonogramWyn.objects.all()
