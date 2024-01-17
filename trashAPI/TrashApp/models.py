# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TblBinLogs(models.Model):
    id_log = models.AutoField(unique=True, primary_key=True)
    date_log = models.TextField()
    bin_id = models.IntegerField()
    bin_status = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tbl_bin_logs'


class TblHarmonogramWyn(models.Model):
    id_daty = models.AutoField(unique=True, primary_key=True)
    data = models.TextField()
    bin_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_harmonogram_wyn'


class TblKoszeKonfiguracyjna(models.Model):
    id_bin = models.AutoField(unique=True, primary_key=True)
    bin_name = models.TextField(unique=True)
    bin_depth = models.TextField()  # This field type is a guess.
    emp_calendar = models.IntegerField()
    emp_reminder = models.IntegerField()
    adding_points = models.IntegerField()
    subtrack_points = models.IntegerField()
    bin_status = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tbl_kosze_konfiguracyjna'


class TblUzytkownicyKonfig(models.Model):
    id_user = models.AutoField(unique=True, primary_key=True)
    user_name = models.TextField(unique=True)
    user_mail = models.TextField()
    statistics_days = models.IntegerField()
    which_bin = models.TextField()
    points_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_uzytkownicy_konfig'


class TblWynoszenie(models.Model):
    id_empty = models.AutoField(unique=True, primary_key=True)
    which_bin = models.IntegerField()
    who_should = models.IntegerField()
    who_did = models.IntegerField()
    date = models.TextField()
    add_points = models.IntegerField(blank=True, null=True)
    sub_points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_wynoszenie'
