from django.db import models
from moto_user.models import MotoUser

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    # slug = models.SlugField(unique=True)
    description = models.TextField()
    time_required = models.CharField(max_length=10)
    instruction = models.TextField()
    author = models.ForeignKey(
        MotoUser,
        on_delete=models.SET_NULL,
        related_name="recipes",
        null=True
        )
    image = models.ImageField(
        upload_to ="recipes",
        null = True,
        blank = True
        )
    date = models.DateTimeField(auto_now=True)
    tags= models.ManyToManyField(Tag, blank=True, related_name='tags')
    favorites = models.ManyToManyField('Recipe', blank=True, related_name='favorite_recipes')


    def __str__(self):
        return f"{self.title} (by:{self.author})"
