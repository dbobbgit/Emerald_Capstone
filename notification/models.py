from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from moto_user.models import MotoUser


# Create your models here.
class Notification(models.Model):
    receiver = models.ForeignKey(
        MotoUser,
        on_delete=models.CASCADE)
    post_to_notify = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
