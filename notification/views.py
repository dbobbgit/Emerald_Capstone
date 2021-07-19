from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Notification
from moto_user.models import MotoUser
from post.models import Post
from recipe.models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'notification/list.html'
    context_object_name = 'notices'
    login_url = 'accounts/login'

    def get_queryset(self):
        return Notification.objects.all()
        # return self.request.user.notifications.unread()


class PostNotificationUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id)')
        if notice_id:
            post = Post.objects.get(id=request.GET.get('post_id'))
            request.user.notification.get(id=notice_id).mark_as_read()
            return redirect(post)
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notification:list')


class RecipeNotificationUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id)')
        if notice_id:
            recipe = Recipe.objects.get(id=request.GET.get('recipe_id'))
            request.user.notification.get(id=notice_id).mark_as_read()
            return redirect(recipe)
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notification:list')

# Create your views here.
# def notification_view(request):
#     try:
#         users = MotoUser.objects.all()
#         print(request.user)
#         user = MotoUser.objects.get(username=request.user)
#         return render(
#             request, 'notification/notify.html', {'users': users, 'user': user}
#             )
#     except Exception as e:
#         print(e)
#         return redirect('home.html')


# def message(request):
#     try:
#         if request.method == 'POST':
#             # sender = MotoUser.objects.get(username=request.user)
#             sender = get_object_or_404(MotoUser, username=request.user)
#             receiver = MotoUser.objects.get(id=request.POST.get('user_id'))
#             notify.send(
#                 sender,
#                 recipient=receiver,
#                 verb='Notification',
#                 description=request.POST.get('message')
#                 )
#             return redirect('home')
#     except Exception:
#         return HttpResponse("Please login from admin site for sending a message")