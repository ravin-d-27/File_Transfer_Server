from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import UploadedFile
from .forms import FileUploadForm
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import Sum


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)

    # Calculate total file size for the user
    total_file_size_bytes = sum(file.file.size for file in files)

    # Convert total file size to KB or MB if needed
    total_file_size_kb = total_file_size_bytes / 1024
    total_file_size_mb = total_file_size_kb / 1024
    total_file_size_mb = round(total_file_size_mb, 2)
    
    return render(request, 'files/file_list.html', {'files': files, 'total_file_size_mb': total_file_size_mb})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user

            # Check if the user is 'sampleuser' and if the total file size exceeds 5 MB
            if request.user.username == 'sampleuser':
                files = UploadedFile.objects.filter(user=request.user)
                total_file_size_bytes = sum(file.file.size for file in files) + request.FILES['file'].size
                total_file_size_mb = total_file_size_bytes / (1024 * 1024)

                if total_file_size_mb > 5:
                    return render(request, 'files/upload_file.html', {'form': form, 'error': 'You have exceeded the 5 MB storage limit.'})
            
            file_instance.save()
            return redirect('files:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'files/upload_file.html', {'form': form})


@login_required
def download_file(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    response = HttpResponse(file_instance.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={file_instance.file.name}'
    return response

# views.py

@login_required
def delete_file(request, unique_token):
    # Try to find the file by unique_token
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)

    # If file_instance is not found, try to find by hashed_file_id
    if not file_instance:
        hashed_file_id = unique_token
        try:
            file_instance = UploadedFile.objects.get(hashed_file_id=hashed_file_id)
        except UploadedFile.DoesNotExist:
            return HttpResponse("File not found.", status=404)

    storage = S3Boto3Storage()
    file_path = file_instance.file.name

    if storage.exists(file_path):
        storage.delete(file_path)

    file_instance.delete()

    files = UploadedFile.objects.filter(user=request.user)
    return redirect('files:file_list')



@login_required
def view_file(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    file_path = file_instance.file.name
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return FileResponse(file_instance.file, content_type='image/'+file_extension)
    elif file_extension == 'pdf':
        response = FileResponse(file_instance.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_instance.file.name}'
        return response
    else:
        return redirect('files:download_file', file_id=file_instance.id)
    
def share_file(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    share_link = request.build_absolute_uri(file_instance.get_share_url())
    modified_url = share_link.replace('share_file', 'share_file_2')
    return render(request, 'files/share_file.html', {'share_link': modified_url})

def share_file_2(request, unique_token):
    file_instance = get_object_or_404(UploadedFile, unique_token=unique_token)
    file_path = file_instance.file.name
    file_extension = file_path.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        return FileResponse(file_instance.file, content_type='image/'+file_extension)
    elif file_extension == 'pdf':
        response = FileResponse(file_instance.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={file_instance.file.name}'
        return response
    else:
        return redirect('files:download_file', unique_token=unique_token)
