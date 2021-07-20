from django import forms
from .models import MotoUser
from django.contrib.auth import get_user_model

User = get_user_model()

class EditProfileForm(forms.Form):

    riding_style_choices = [
            ('RIDING_STYLE_EXAMPLE1', 'riding_style_example1'),
            ('RIDING_STYLE_EXAMPLE2', 'riding_style_example2'),
            ('RIDING_STYLE_EXAMPLE3', 'riding_style_example3'),
        ]

    riding_level_choices = [
        ('RIDING_LEVEL_EXAMPLE1', 'riding_level_example1'),
        ('RIDING_LEVEL_EXAMPLE2', 'riding_level_example2'),
        ('RIDING_LEVEL_EXAMPLE3', 'riding_level_example3'),
        ]

    avatar = forms.ImageField(required=False)
    display_name = forms.CharField(max_length=30)
    bio = forms.CharField(max_length=300)
    bike = forms.CharField(max_length=50)
    riding_style = forms.ChoiceField(choices=riding_style_choices)
    riding_level = forms.ChoiceField(choices=riding_level_choices)
