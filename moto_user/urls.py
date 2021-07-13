from django.urls import path, include
from . import views


urlpatterns = [
    path('profile/<int:user_id>/', views.MotoUserView, name='MotoUserView'),
    path('edit/profile/<int:user_id>/', views.EditProfileView, name='EditProfileView')
]