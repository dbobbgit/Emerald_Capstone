from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(CustomUser, UserAdmin)