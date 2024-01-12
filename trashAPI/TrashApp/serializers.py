from rest_framework import serializers
from TrashApp.models import *

class TblUzytkownicyKonfigSerializer(serializers.ModelSerializer):
     class Meta:
        model = TblUzytkownicyKonfig
        fields = '__all__'

class TblKoszeKonfiguracyjnaSerializer(serializers.ModelSerializer):
     class Meta:
        model = TblKoszeKonfiguracyjna
        fields = '__all__'

class TblBinLogsSerializer(serializers.ModelSerializer):
     class Meta:
        model = TblBinLogs
        fields = '__all__'


class TblHarmonogramWynSerializer(serializers.ModelSerializer):
     class Meta:
        model = TblHarmonogramWyn
        fields = '__all__'


class TblWynoszenieSerializer(serializers.ModelSerializer):
    class Meta:
        model=TblWynoszenie
        fields = '__all__'