from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MotoUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MotoUser
    list_display = ['username', 'email', 'password', 'display_name', 'bio', 'bike', 'riding_style', 'riding_level']


admin.site.register(MotoUser, CustomUserAdmin)
