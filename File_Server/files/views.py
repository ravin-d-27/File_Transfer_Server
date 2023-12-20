# files/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .forms import FileUploadForm

@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'files/file_list.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'files/upload_file.html', {'form': form})
