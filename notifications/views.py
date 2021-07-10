from django.shortcuts import render
from moto_user.models import MotoUser
from post.models import Post
from notifications.models import Notifications
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def notification_view(request):
    notifications = Notifications.objects.filter(
        author=request.user, read=False)
    n_list = []
    for item in notifications:
        if item.read == False:
            n_list.append(item)
            item.read = True
            item.save()
    return render(request, 'notifications/notify.html', {
        'notifications': n_list,
    })