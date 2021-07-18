from django.db import models
from django.contrib.auth.models import AbstractUser
from motogram.settings import AUTH_USER_MODEL


# Create your models here.
class MotoUser(AbstractUser):
    """CAITLIN: THIS CUSTOM USER MODEL IS INTENDED TO BE THE BASIS FOR OUR PROFILE TEMPLATE. 
    OUR ABSTRACT USER PARAMETER GIVES US ACCESS TO USERNAME, PASSWORD, AND EMAIL"""
    
    display_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=300)
    bike = models.CharField(max_length=50)

    riding_style_choices = [
        ('RIDING_STYLE_EXAMPLE1', 'riding_style_example1'),
        ('RIDING_STYLE_EXAMPLE2', 'riding_style_example2'),
        ('RIDING_STYLE_EXAMPLE3', 'riding_style_example3'),
    ]

    riding_style = models.CharField(max_length=21, 
                                    choices=riding_style_choices, 
                                    default="JUST STARTING")

    riding_level_choices = [
        ('RIDING_LEVEL_EXAMPLE1', 'riding_level_example1'),
        ('RIDING_LEVEL_EXAMPLE2', 'riding_level_example2'),
        ('RIDING_LEVEL_EXAMPLE3', 'riding_level_example3'),
    ]

    riding_level = models.CharField(max_length=21, 
                                    choices=riding_level_choices, 
                                    default="JUST STARTING")

    following = models.ManyToManyField('self', symmetrical=False)

    favorite_posts = models.ManyToManyField('post.Post', symmetrical=False, related_name='+', blank=True, null=True)

    favorite_recipes = models.ManyToManyField('recipe.Recipe', symmetrical=False, related_name='+', blank=True, null=True)
    
    
    def __str__(self):
            return self.display_name


