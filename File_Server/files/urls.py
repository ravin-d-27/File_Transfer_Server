# files/urls.py
from django.urls import path
from .views import file_list, upload_file, download_file, delete_file, view_file, share_file_2,share_file

app_name= 'files'
urlpatterns = [
    path('', file_list, name='file_list'),
    path('upload/', upload_file, name='upload_file'),
    path('download/<str:unique_token>/', download_file, name='download_file'),
    path('delete/<str:unique_token>/', delete_file, name='delete_file'),
    path('view_file/<str:unique_token>/', view_file, name='view_file'),
    path('share_file_2/<str:unique_token>/', share_file_2, name='share_file_2'),
    path('share_file/<str:unique_token>/', share_file, name='share_file'),
]
