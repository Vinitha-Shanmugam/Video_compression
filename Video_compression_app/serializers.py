from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
# serializers.py
# from rest_framework import serializers
#
# class VideoUploadSerializer(serializers.Serializer):
#     video = serializers.FileField()
#     compression_size = serializers.CharField()
