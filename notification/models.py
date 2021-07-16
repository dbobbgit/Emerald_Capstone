from django.db import models
from django.db.models.signals import post_save
from moto_user.models import MotoUser
# from post.models import Post


# Create your models here.
class Notification(models.Model):
    receiver = models.ForeignKey(
        MotoUser,
        on_delete=models.CASCADE)
    post_to_notify = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


# def post_notification_signal(sender, instance, created, **kwargs):
#     print(instance, created)
#     if created:
#         Notification.objects.create(post=instance)

# post_save.connect(post_notification_signal, sender=Post)