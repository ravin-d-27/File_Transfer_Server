from django.urls import path
from .views import file_list, upload_file

urlpatterns = [
    path('', file_list, name='file_list'),
    path('upload/', upload_file, name='upload_file'),
]
