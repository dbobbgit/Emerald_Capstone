from django.urls import path
from stories_app.views import NewStory, ShowMedia

urlpatterns = [
    path('newstory/', NewStory, name='newstory'),
    path('showmedia/<stream_id>', ShowMedia, name='showmedia'),
]