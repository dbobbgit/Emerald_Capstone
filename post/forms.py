from django import forms
from django.forms.widgets import TextInput
from post.models import Post
from django.forms import ClearableFileInput, fields

class NewPostForm(forms.ModelForm):
        picture = forms.ImageField(required=True)
        caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
        tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

        class Meta:
            model = Post
            fields = ('picture', 'caption', 'tags')