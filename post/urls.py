from post.views import index, NewPost, post_detail_view
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('post_detail/<int:post_id>/', post_detail_view)

]
