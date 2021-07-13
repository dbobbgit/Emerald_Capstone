from django.http.response import HttpResponse
from post.models import Post, Stream
from django.contrib.auth.decorators import login_required
from django.template import loader


@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.order_by('-posted')
    template = loader.get_template('index.html')
    context = {'post_items': post_items, }
    return HttpResponse(template.render(context, request))

# Create your views here.
