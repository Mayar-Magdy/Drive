from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import UploadedFile
from .serializers import FileUploadSerializer
from django.utils import timezone


class FileUploadView(APIView):
    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if len(files) > 10:
            return Response({"error": "You can upload up to 10 files per request."}, status=400)

        total_size = sum(f.size for f in files)
        if total_size + self.get_user_total_size(request.user) > 1 * 1024 * 1024 * 1024:  # 1 GB per day
            return Response({"error": "Total file size exceeds daily limit of 1 GB."}, status=400)

        uploaded_files = []
        for file in files:
            serializer = FileUploadSerializer(data={'file': file, 'category': self.get_category(file)})
            if serializer.is_valid():
                uploaded_file = serializer.save(user=request.user, size=file.size)
                uploaded_files.append(uploaded_file)
            else:
                return Response(serializer.errors, status=400)

        return Response({"uploaded_files": [str(f) for f in uploaded_files]}, status=201)

    def get_user_total_size(self, user):
        from django.db.models import Sum
        today = timezone.now().date()
        return UploadedFile.objects.filter(user=user, upload_date__date=today).aggregate(Sum('size'))['size__sum'] or 0

    def get_category(self, file):
        if file.content_type.startswith('image'):
            return 'Image'
        elif file.content_type.startswith('video'):
            return 'Video'
        return 'Document'

class FileListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files = UploadedFile.objects.filter(user=request.user)
        return Response({"files": [{"id": f.id, "name": f.file.name, "category": f.category} for f in files]})


class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, file_id, *args, **kwargs):
        try:
            file = UploadedFile.objects.get(id=file_id, user=request.user)
            file.delete()
            return Response({"message": "File deleted successfully."}, status=200)
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found."}, status=404)


from django.db.models import Count, Sum

class FileAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files = UploadedFile.objects.filter(user=request.user)
        analytics = files.values('category').annotate(
            total_files=Count('id'),
            total_size=Sum('size')
        )
        overall_size = files.aggregate(Sum('size'))['size__sum'] or 0
        return Response({"analytics": analytics, "overall_size": overall_size})


