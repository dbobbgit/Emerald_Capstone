from django import forms 
from stories_app.models import Story
from django.forms import ClearableFileInput

class NewStoryForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Story
        fields = ('content', 'caption')