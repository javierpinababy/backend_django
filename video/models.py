import os
from django.db import models
from django.contrib.auth.models import User


def upload_video_path(instance, filename):
    print(f"filename: {filename}")
    old_instance = Video.objects.get(pk=instance.pk)
    old_instance.video.delete()
    return "video/" + filename


def upload_image_path(instance, filename):
    old_instance = Video.objects.get(pk=instance.pk)
    old_instance.video.delete()
    return "image_video/" + filename


class Video(models.Model):
    description = models.TextField()
    video = models.FileField(upload_to=upload_video_path)
    image = models.ImageField(upload_to=upload_image_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_counter = models.IntegerField(default=0)
    likes_counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
