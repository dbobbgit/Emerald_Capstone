from django import forms
from moto_user.models import MotoUser
from recipe.models import Recipe


class CreateRecipeForm(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=30)
    instructions = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=MotoUser.objects.all())


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'time_required',
            'instruction'
        ]