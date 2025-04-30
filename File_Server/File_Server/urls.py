from django.contrib import admin
from django.urls import include, path
import accounts.views as acviews

import files.views as fviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acviews.home, name='home'),
    path('files/', include('files.urls')),
    path('login/', acviews.login, name='login'),
    path('logout/', acviews.logout, name='logout'),
    path('activity/', include('activity.urls')),
    path('notes/', fviews.notes_dashboard, name='dashboard'),
    path('save/', fviews.save_notes, name='save_notes'),
    path('<int:note_id>/delete/', fviews.delete_note, name='delete_note'),
]
