
from django.urls import path
from .views import FileUploadView, FileListView, FileDeleteView, FileAnalyticsView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('delete/<int:file_id>/', FileDeleteView.as_view(), name='file-delete'),
    path('analytics/', FileAnalyticsView.as_view(), name='file-analytics'),
]
