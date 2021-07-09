from django.db import models
from post.models import Post
from moto_user import MotoUser
from notifications import Notifications

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user
        notify = Notifications(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notifications(post=post, sender=sender, notification_type=2)
        notify.delete()