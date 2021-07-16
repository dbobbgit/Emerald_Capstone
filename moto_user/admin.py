from django.contrib import admin


# Register your models here.

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from moto_user.models import MotoUser
from motogram.settings import AUTH_USER_MODEL
# Register your models here.
UserAdmin.fieldsets += (
    'additional information',{'fields':('bio', 'display_name', 'bike', 'riding_style', 'riding_level', 'favorite_posts', 'favorite_recipes', 'following')}
),
admin.site.register(MotoUser, UserAdmin)

