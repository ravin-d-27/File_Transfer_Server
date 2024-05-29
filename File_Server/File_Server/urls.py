from django.contrib import admin
from django.urls import include, path
import accounts.views as acviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acviews.home, name='home'),
    path('files/', include('files.urls')),
    path('login/', acviews.login, name='login'),
    path('logout/', acviews.logout, name='logout'),
    path('activity/', include('activity.urls')),
]
