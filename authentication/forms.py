from django import forms
from user.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
