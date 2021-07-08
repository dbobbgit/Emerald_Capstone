from django.apps import AppConfig
from motogram.settings import AUTH_USER_MODEL


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moto_user'
