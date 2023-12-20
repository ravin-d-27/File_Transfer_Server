from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def home(request):
    return render(request,'accounts/home.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')

        else:
            return render(request,'accounts/login.html',{'error':"Your username or password is incorrect!"})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')