from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MotoUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MotoUser

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Info',
            {
                'fields': (
                    'bio',
                    'display_name',
                    'bike',
                    'riding_style',
                    'riding_level',
                    'avatar'
                    )}))

    exclude = ['password2']


admin.site.register(MotoUser, CustomUserAdmin)
