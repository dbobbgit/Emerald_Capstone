from django.shortcuts import render
from user.models import CustomUser
# Create your views here.


def profile_view(request, user_id:int):
    current_user = CustomUser.objects.get(id=user_id)
    return render(request, 'profile.html', {'current_user':current_user })