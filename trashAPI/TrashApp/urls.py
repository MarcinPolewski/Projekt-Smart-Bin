from django.conf.urls import url
from TrashApp import views
from TrashApp.views import *
from rest_framework import routers

api_pefix ="api/"


router = routers.DefaultRouter()
router.register(api_pefix + r'users', UserViewSet)
router.register(api_pefix + r'bins', BinViewSet)
router.register(api_pefix + r'logs', LogsViewSet)
router.register(api_pefix + r'takeout', TakeoutViewSet)
router.register(api_pefix + r'schedule', ScheduleViewSet)
urlpatterns = [
    url(r'^users/$', views.userApi),
    url(r'^users/([0-9]+)', views.userApi),
    url(r'^bins/$', views.binApi),
    url(r'^bins/([0-9]+)', views.binApi),
    url(r'^logs/$', views.logsApi),
    url(r'^logs/([0-100]+)', views.logsApi),
    url(r'^schedule/$', views.scheduleApi),
    url(r'^schedule/([0-100]+)', views.scheduleApi),
    url(f'^takeout/$', views.takeoutApi),
    url(r'^takeout/([0-9]+)', views.takeoutApi)
]

urlpatterns += router.urls