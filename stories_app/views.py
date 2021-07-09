from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from stories_app.models import Story, StoryStream
from stories_app.forms import NewStoryForm

@login_required
def NewStory(request):
    user = request.user
    files_objs = []

    if request.method == 'POST':
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('content')
            caption = form.cleaned_data.get('caption')
            story = Story(user=user, content=file, caption=caption)
            story.save()
            return redirect('index')
    else:
        form = NewStoryForm()
        context = {'form': form,}
        return render(request, 'newstory.html', context)


def ShowMedia(request, stream_id):
    stories = StoryStream.objects.get(id=stream_id)
    media_st = stories.story.all().values()
    stories_list = list(media_st)
    return JsonResponse(stories_list, safe=False)
# Create your views here.
