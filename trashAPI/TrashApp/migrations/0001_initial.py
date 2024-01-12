# Generated by Django 3.2.23 on 2024-01-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblBinLogs',
            fields=[
                ('id_log', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date_log', models.TextField()),
                ('bin_id', models.IntegerField()),
                ('bin_status', models.TextField()),
            ],
            options={
                'db_table': 'tbl_bin_logs',
            },
        ),
        migrations.CreateModel(
            name='TblHarmonogramWyn',
            fields=[
                ('id_daty', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('data', models.TextField()),
                ('bin_id', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_harmonogram_wyn',
            },
        ),
        migrations.CreateModel(
            name='TblKoszeKonfiguracyjna',
            fields=[
                ('id_bin', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('bin_name', models.TextField(unique=True)),
                ('bin_depth', models.TextField()),
                ('emp_calendar', models.IntegerField()),
                ('emp_reminder', models.IntegerField()),
                ('adding_points', models.IntegerField()),
                ('subtrack_points', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_kosze_konfiguracyjna',
            },
        ),
        migrations.CreateModel(
            name='TblUzytkownicyKonfig',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('user_name', models.TextField(unique=True)),
                ('user_mail', models.TextField()),
                ('statistics_days', models.IntegerField()),
                ('which_bin', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_uzytkownicy_konfig',
            },
        ),
        migrations.CreateModel(
            name='TblWynoszenie',
            fields=[
                ('id_empty', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('which_bin_field', models.IntegerField(db_column='which_bin_')),
                ('who_should', models.IntegerField()),
                ('who_did', models.IntegerField()),
                ('date', models.TextField()),
                ('add_points', models.IntegerField(blank=True, null=True)),
                ('sub_points', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_wynoszenie',
            },
        ),
    ]