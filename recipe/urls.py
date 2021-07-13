from django.urls import path
from . import views


urlpatterns = [
    path('', views.Recipe_List_View, name='recipe'),
    path('<slug:slug>', views.Recipe_detail_view.as_view(), name='recipe-detail')
]
