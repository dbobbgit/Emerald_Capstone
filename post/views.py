from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from post.models import Post, Tag
from django.contrib.auth.decorators import login_required
from django.template import loader
from post.forms import NewPostForm
from django.template import RequestContext


@login_required
def index(request):
    posts = Post.objects.all().order_by('-posted')
    template = loader.get_template('home.html')
    context = {'post_items': posts, }
    return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')
            tags_list = list(tags_form.split(','))
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('home')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }
    return render(request, 'newpost.html', context)


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
