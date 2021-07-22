from django.db import models
from moto_user.models import MotoUser
from django.db.models import Q


class RecipeManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)|
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Recipe(models.Model):
    title = models.CharField(max_length=50)
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
        upload_to="recipes",
        null=True,
        blank=True
        )
    date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    favorites = models.ManyToManyField('Recipe', blank=True, related_name='favorite_recipes')
    comment = models.ManyToManyField('Comment', blank=True, related_name='comment')

    def __str__(self):
        return f"{self.title} (by:{self.author})"


class Comment (models.Model):
    text = models.CharField(max_length=150)
    author = models.ForeignKey(
        MotoUser, 
        related_name='commenter',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    recipe_post = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
        )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
