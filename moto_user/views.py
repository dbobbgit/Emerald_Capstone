from django.shortcuts import render
from moto_user.models import MotoUser
from motogram.settings import AUTH_USER_MODEL
# Create your views here.


def profile_view(request, user_id:int):
    current_user = MotoUser.objects.get(id=user_id)
    return render(request, 'profile.html', {'current_user':current_user })