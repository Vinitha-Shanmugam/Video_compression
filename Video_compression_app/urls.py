# urls.py
from django.urls import path
from .views import VideoCompressionView

urlpatterns = [
    path('upload/', VideoCompressionView.as_view(), name='video-upload'),
]
