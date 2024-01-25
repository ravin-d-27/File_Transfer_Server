# files/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    # Add a new field to store the unique token
    unique_token = models.CharField(max_length=32, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique token for the file
        if not self.unique_token:
            self.unique_token = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"