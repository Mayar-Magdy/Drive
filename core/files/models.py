from django.db import models
from django.conf import settings

class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Document', 'Document'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
