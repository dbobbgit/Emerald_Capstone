from django.db import models
from moto_user.models import MotoUser

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Author(models.Model):
    author = models.OneToOneField(MotoUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    time_required = models.CharField(max_length=10)
    instruction = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        related_name="recipes",
        null=True
        )
    image = models.ImageField(
        ("static/recipe/images/"),
        upload_to ="recipes",
        null = True,
        )
    date = models.DateField(auto_now=True)
    tags= models.ManyToManyField(Tag)
    favorites = models.ManyToManyField('Recipe', blank=True, related_name='favorite_recipes')


    def __str__(self):
        return f"{self.title} (by:{self.author})"
