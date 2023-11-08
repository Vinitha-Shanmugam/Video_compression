from django.db import models


class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    size_limit = models.CharField(max_length=10, default='10MB')


