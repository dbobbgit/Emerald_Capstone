from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('list/', views.NotificationListView.as_view(), name='list'),
    path('post_update/', views.PostNotificationUpdateView.as_view(), name='post_update'),
    path('recipe_update/', views.RecipeNotificationUpdateView.as_view(), name='recipe_update'),
]
