# files/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .forms import FileUploadForm
import os

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

@login_required
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    response = HttpResponse(file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={file.file.name}'
    return response


@login_required
def delete_file(request, file_id):
    file_instance = get_object_or_404(UploadedFile, id=file_id)

    file_path = file_instance.file.path
    if os.path.exists(file_path):
        os.remove(file_path)

    file_instance.delete()

    return redirect('file_list')