from rest_framework import serializers
from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'category']

    def validate_file(self, file):
        allowed_types = ['image', 'video', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        max_file_size = 100 * 1024 * 1024  # 100 MB

        if file.content_type.split('/')[0] not in allowed_types and file.content_type not in allowed_types:
            raise serializers.ValidationError("Invalid file type.")
        if file.size > max_file_size:
            raise serializers.ValidationError("File size exceeds the maximum limit of 100 MB.")
        return file
