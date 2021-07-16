from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    # path('', views.Recipe_List_View, name='recipe'),
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('<slug:slug>', views.Recipe_detail_view.as_view(), name='recipe-detail'),
    path('<slug:slug>/edit', views.RecipeEditView.as_view(), name='edit-recipe'),
    path('<slug:slug>/delete', views.RecipeDeleteView.as_view(), name='delete-recipe')
]
