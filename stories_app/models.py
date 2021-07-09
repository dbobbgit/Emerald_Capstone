from django.db import models
from moto_user import MotoUser
from post.models import Follow


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Story(models.Model):
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE, related_name='story_user')
    content = models.FileField(upload_to=user_directory_path)
    caption = models.TextField(max_length=60)
    expired = models.BooleanField(default=False)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class StoryStream(models.Model):
    following = models.ForeignKey(MotoUser, on_delete=models.CASCADE, related_name='story_following')
    user = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    story = models.ManyToManyField(Story, related_name='stories')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.following.username + ' - ' + str(self.date)

    def add_post(sender, instance, *args, **kwargs):
        new_story = instance
        user = new_story.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            try:
                s = StoryStream.objects.get(user=follower.follower, following=user)
            except StoryStream.DoesNotExist:
                s = StoryStream.objects.create(user=follower.follower, date=new_story.posted, following=user)
            s.story.add(new_story)
            s.save()