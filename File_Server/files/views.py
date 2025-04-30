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
    files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    # Calculate total file size for the user
    total_file_size_bytes = sum(file.file.size for file in files)

    # Convert total file size to KB or MB if needed
    total_file_size_kb = total_file_size_bytes / 1024
    total_file_size_mb = total_file_size_kb / 1024
    total_file_size_mb = round(total_file_size_mb, 2)
    
    if total_file_size_mb==0:    
        return render(request, 'files/file_list.html', {'files': files, 'total_file_size_mb': total_file_size_mb,'message_zero':"⚠️ You have not uploaded any files ! ⚠️"})
    else:
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
    return render(request,'accounts/home.html',{'delete_success':"The file {} is Deleted Successfully".format(file_path)})



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






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Note

@login_required
def notes_dashboard(request):
    """View for the notes dashboard page"""
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'files/notes_page.html', {'notes': notes})

@login_required
@require_POST
def save_notes(request):
    """API endpoint to save all notes"""
    try:
        data = json.loads(request.body)
        notes_data = data.get('notes', [])
        
        updated_notes = []
        
        for note_data in notes_data:
            note_id = note_data.get('id')
            title = note_data.get('title', '').strip() or 'Untitled Note'
            content = note_data.get('content', '')
            
            # For existing notes
            if note_id and not note_id.startswith('new-'):
                try:
                    note = Note.objects.get(id=note_id, user=request.user)
                    note.title = title
                    note.content = content
                    note.save()
                except Note.DoesNotExist:
                    # Skip if the note doesn't exist or doesn't belong to the user
                    continue
            # For new notes
            else:
                note = Note.objects.create(
                    user=request.user,
                    title=title,
                    content=content
                )
                updated_notes.append({
                    'old_id': note_id,
                    'new_id': note.id,
                    'updated_at': note.updated_at.strftime('%b %d, %Y %H:%M')
                })
        
        return JsonResponse({
            'success': True,
            'updated_notes': updated_notes
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def delete_note(request, note_id):
    """API endpoint to delete a note"""
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)