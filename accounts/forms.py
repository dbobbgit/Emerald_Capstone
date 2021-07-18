from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

        exclude = ['password2']


class CustomUserChangeForm(UserChangeForm):
    password2 = None
    
    class Meta:
        model = User
        fields = ('username', 'password')

        exclude = ['password2']