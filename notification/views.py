from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from moto_user.models import MotoUser
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save


# Create your views here.
def notification_view(request):
    try:
        users = MotoUser.objects.all()
        print(request.user)
        user = MotoUser.objects.get(username=request.user)
        return render(
            request, 'notification/notify.html', {'users': users, 'user': user}
            )
    except Exception as e:
        print(e)
        return redirect('home.html')


def message(request):
    try:
        if request.method == 'POST':
            # sender = MotoUser.objects.get(username=request.user)
            sender = get_object_or_404(MotoUser, username=request.user)
            receiver = MotoUser.objects.get(id=request.POST.get('user_id'))
            notify.send(
                sender,
                recipient=receiver,
                verb='Notification',
                description=request.POST.get('message')
                )
            return redirect('home')
    except Exception:
        return HttpResponse("Please login from admin site for sending a message")