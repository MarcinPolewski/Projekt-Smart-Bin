from django.urls import path
from TrashApp import views
from TrashApp.views import *
from rest_framework import routers

api_prefix = "api/"

router = routers.DefaultRouter()
router.register(api_prefix + r'users', UserViewSet)
router.register(api_prefix + r'bins', BinViewSet)
router.register(api_prefix + r'logs', LogsViewSet)
router.register(api_prefix + r'takeout', TakeoutViewSet)
router.register(api_prefix + r'schedule', ScheduleViewSet)

urlpatterns = [
    path('users/', views.userApi),
    path('users/<int:pk>/', views.userApi),
    path('bins/', views.binApi),
    path('bins/<int:pk>/', views.binApi),
    path('logs/', views.logsApi),
    path('logs/<int:pk>/', views.logsApi),
    path('schedule/', views.scheduleApi),
    path('schedule/<int:pk>/', views.scheduleApi),
    path('takeout/', views.takeoutApi),
    path('takeout/<int:pk>/', views.takeoutApi),
]

urlpatterns += router.urls
