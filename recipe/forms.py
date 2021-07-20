from django import forms
from moto_user.models import MotoUser
from recipe.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        labels = {
            'title': "Recipe name",
            'description': "Description",
            'time_required': "Duration time",
            'instruction': "Detail of your recipe",
            'image': "Share your image",
        }
        exclude = ['date', 'favorites', 'tags', 'author', 'password2']



class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'time_required',
            'instruction'
        ]

        exclude = ['password2']