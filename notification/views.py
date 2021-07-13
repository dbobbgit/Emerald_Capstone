from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from moto_user.models import MotoUser
from post.models import Post
# from notifications.models import Notifications
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from notifications.signals import notify


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


# @login_required
# def notification_view(request):
#     notifications = Notifications.objects.filter(
#         author=request.user, read=False)
#     n_list = []
#     for item in notifications:
#         if item.read == False:
#             n_list.append(item)
#             item.read = True
#             item.save()
#             messages.success(request, 'Message has been sent!!')
#     return render(request, 'notifications/notify.html', {
#         'notifications': n_list,
#         'authour': MotoUser
#     })


# def delete_notification(request, notify_id):
#     notifications = Notifications.objects.get(id=notify_id)
#     notifications.read = True
#     notifications.save()
#     messages.success(request, 'Message has been sent!!')
#     return redirect('notifications/notify.html',)