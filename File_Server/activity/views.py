# activity/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserActivity

@login_required
def activity_log(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'activity/activity_log.html', {'activities': activities})