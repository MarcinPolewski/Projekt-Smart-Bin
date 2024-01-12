from django.conf.urls import url
from TrashApp import views


urlpatterns = [
    url(r'^users/$', views.userApi),
    url(r'^users/([0-9]+)', views.userApi),
    url(r'^bins/$', views.binApi),
    url(r'^bins/([0-9]+)', views.userApi),
    url(r'^logs/$', views.logsApi),
    url(r'^logs/([0-100]+)', views.userApi),
    url(r'^schedule/$', views.scheduleApi),
    url(r'^schedule/([0-100]+)', views.userApi),
    url(f'^takeout/$', views.takeoutApi),
    url(r'^takeout/([0-100]+)', views.userApi),
]