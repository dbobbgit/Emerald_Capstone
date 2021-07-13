from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('notice_list/', views.notification_view, name='notice')
]
