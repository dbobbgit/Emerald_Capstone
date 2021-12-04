import uuid
# https://www.geeksforgeeks.org/uuidfield-django-models/
from django.db import models
from django.utils import timezone
from moto_user.models import MotoUser
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
from notification.models import Notification


''' This funcion allows the file to be uploaded to MEDIA_ROOT/user_<id>/<filename>'''


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


''' Creating models for our tags'''


class Tag(models.Model):
    title = models.CharField(max_length=80, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PostFileContent(models.Model):
    user = models.ForeignKey(
        MotoUser,
        on_delete=models.CASCADE, 
        related_name='content_owner'
        )
    file = models.FileField(upload_to=user_directory_path)


class Post(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='Picture',
        null=False
        )
    # content = models.ManyToManyField(PostFileContent, related_name='contents')
    caption = models.TextField(max_length=500, verbose_name='Caption')
    posted = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

# TODO: Beginning of implementation of followERS count
# class Follow(models.Model):
#     follower = models.ForeignKey(
#         MotoUser,
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='follower'
#         )
#     following = models.ForeignKey(
#         MotoUser,
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='following'
#         )

#     def user_follow(sender, instance, *args, **kwargs):
#         follow = instance
#         sender = follow.follower
#         following = follow.following
#         notify = Notification(sender=sender, user=following, notification_type=3)
#         notify.save()

#     def user_unfollow(sender, instance, *args, **kwargs):
#         follow = instance
#         sender = follow.follower
#         following = follow.following
#         notify = Notification(sender=sender, user=following, notification_type=3)
#         notify.delete()


class Stream(models.Model):
    following = models.ForeignKey(MotoUser, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower, date=post.posted, following=user)
            stream.save()

class Likes(models.Model):
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(MotoUser, on_delete=models.CASCADE, related_name='post_like')

    def user_like_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.delete()
