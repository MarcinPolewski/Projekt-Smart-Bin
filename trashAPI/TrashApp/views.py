from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from TrashApp.models import *
from TrashApp.serializers import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.


@csrf_exempt
def userApi(request, id=0):
    if request.method =="GET":
        user = TblUzytkownicyKonfig.objects.all()
        user_serializer = TblUzytkownicyKonfigSerializer(user, many=True)
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method == "POST":
        user_data=JSONParser().parse(request)
        user_serializer = TblUzytkownicyKonfigSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        user=TblUzytkownicyKonfig.objects.get(id_user=user_data['id_user'])
        user_serializer = TblUzytkownicyKonfigSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method=='DELETE':
        user= TblUzytkownicyKonfig.objects.get(id_user=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)




@csrf_exempt
def binApi(request, id=0):
    if request.method =="GET":
        user = TblKoszeKonfiguracyjna.objects.all()
        user_serializer = TblKoszeKonfiguracyjnaSerializer(user, many=True)
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method == "POST":
        user_data=JSONParser().parse(request)
        user_serializer = TblKoszeKonfiguracyjnaSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        user=TblKoszeKonfiguracyjna.objects.get(id_bin=user_data['id_bin'])
        user_serializer = TblKoszeKonfiguracyjnaSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method=='DELETE':
        user= TblKoszeKonfiguracyjna.objects.get(id_bin=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def logsApi(request, id=0):
    if request.method =="GET":
        user = TblBinLogs.objects.all()
        user_serializer = TblBinLogsSerializer(user, many=True)
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method == "POST":
        user_data=JSONParser().parse(request)
        user_serializer = TblBinLogsSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        user=TblBinLogs.objects.get(id_log=user_data['id_log'])
        user_serializer =TblBinLogsSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method=='DELETE':
        user= TblBinLogs.objects.get(id_log=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)



@csrf_exempt
def scheduleApi(request, id=0):
    if request.method =="GET":
        user = TblHarmonogramWyn.objects.all()
        user_serializer = TblHarmonogramWynSerializer(user, many=True)
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method == "POST":
        user_data=JSONParser().parse(request)
        user_serializer = TblHarmonogramWynSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        user=TblHarmonogramWyn.objects.get(id_daty=user_data['id_daty'])
        user_serializer =TblHarmonogramWynSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succseful", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method=='DELETE':
        user= TblHarmonogramWyn.objects.get(id_daty=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)


@csrf_exempt
def takeoutApi(request, id=0):
    if request.method =="GET":
        takeout = TblWynoszenie.objects.all()
        takeout_serializer = TblWynoszenieSerializer(takeout, many=True)
        return JsonResponse(takeout_serializer.data,safe=False)
    elif request.method == "POST":
        user_data=JSONParser().parse(request)
        print(user_data)
        user_serializer = TblWynoszenieSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added succesfully",safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=="PUT":
        user_data=JSONParser().parse(request)
        user=TblWynoszenie.objects.get(id_empty=user_data['id_empty'])
        user_serializer =TblWynoszenieSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated succsefully", safe=False)
        return JsonResponse("update failed", safe=False)
    elif request.method=='DELETE':
        user= TblWynoszenie.objects.get(id_empty=id)
        user.delete()
        return JsonResponse("deleted succesfully", safe=False)



class UserViewSet(ModelViewSet):
    serializer_class=TblUzytkownicyKonfigSerializer
    queryset=TblUzytkownicyKonfig.objects.all()



class BinViewSet(ModelViewSet):
    serializer_class=TblKoszeKonfiguracyjnaSerializer
    queryset=TblKoszeKonfiguracyjna.objects.all()


class LogsViewSet(ModelViewSet):
    serializer_class=TblBinLogsSerializer
    queryset=TblBinLogs.objects.all()

class TakeoutViewSet(ModelViewSet):
    serializer_class=TblWynoszenieSerializer
    queryset=TblWynoszenie.objects.all()

class ScheduleViewSet(ModelViewSet):
    serializer_class=TblHarmonogramWynSerializer
    queryset=TblHarmonogramWyn.objects.all()



