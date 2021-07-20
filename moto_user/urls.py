from django.urls import path, include
from . import views


urlpatterns = [
    path('profile/<int:user_id>/', views.MotoUserView, name='MotoUserView'),
    path('edit/profile/<int:user_id>/', views.EditProfileView, name='EditProfileView'),
    path("favorite_post/<str:post_id>/", views.Add_Favorite_Post, name='AddFavePost'),
    path("unfavorite_post/<str:post_id>/", views.Remove_Favorite_Post, name='RemoveFavePost'),
    path("favorite_recipe/<int:recipe_pk>/", views.Add_Favorite_Recipe, name='AddFaveRecipe'),
    path("unfavorite_recipe/<int:recipe_pk>/", views.Remove_Favorite_Recipe, name='RemoveFaveRecipe'),
    path("follow/<int:user_id>/", views.Follow_View, name='FollowView'),
    path("unfollow/<int:user_id>/", views.Unfollow_View, name='UnfollowView'),
    path('following/all/<int:user_id>/', views.Following_View, name='FollowingList')
]