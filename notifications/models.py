from django.db import models
from user.models import CustomUser
from post.models import Post

# Create your models here.
class Notifications(models.Model):
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE)
    text = models.ForeignKey(
        Post, 
        on_deleate=models.CASCADE)
    visibility = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null = True)
    