# activity/urls.py
from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('activity-log/', views.activity_log, name='activity_log'),
]
