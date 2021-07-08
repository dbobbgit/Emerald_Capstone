from django.db import models
from moto_user.models import MotoUser
from post.models import Post

# Create your models here.
class Notifications(models.Model):
    author = models.ForeignKey(
        MotoUser, 
        on_delete=models.CASCADE)
    text = models.ForeignKey(
        Post, 
        on_deleate=models.CASCADE)
    read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null = True)
    