from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from moto_user.models import MotoUser
# from post.models import Post


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100, blank=True)
    message = models.TextField(default=False)
    author = models.ForeignKey(
        MotoUser,
        on_delete=models.CASCADE)
    text = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


# @receiver(post_save, sender=MotoUser)
# def create_welcome__message(sender, **kwargs):
#     if kwargs.get('created', False):
#         Notifications.objects.create(
#             author=kwargs.get('instance'),
#             title="Welcome to Motogram!!",
#             message="Thanks for signing up!!"
#         )
