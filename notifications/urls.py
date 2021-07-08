from django.urls import path, include
from . import views

urlpatterns = [
    path('notification/', views.notification_view, name='notifications')
]