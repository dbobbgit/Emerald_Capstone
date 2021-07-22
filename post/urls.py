from post.views import index, NewPost
from django.urls import path

urlpatterns = [
    path('', index, name='home'),
    path('newpost/', NewPost, name='newpost')
]
