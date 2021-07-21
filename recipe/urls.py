from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'), #recipe/
    path('create/', views.create_recipe_view, name='create-recipe'), #recipe/create/
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'), #recipe/number
    path('<int:pk>/edit', views.edit_recipe_view, name='edit-recipe'),
    path('<int:pk>/delete', views.delete_recipe_view, name='delete-recipe') #recipe/number/delete
]