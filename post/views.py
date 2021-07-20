from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from post.models import Post, Tag
from django.contrib.auth.decorators import login_required
from django.template import loader
from post.forms import NewPostForm


""" index created here """
@login_required
def index(request):
    posts = Post.objects.all().order_by('-id')
    template = loader.get_template('index.html')
    context = {'post_items': posts, }
    return HttpResponse(template.render(context, request))


'''New post is created here.'''
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
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }
    return render(request, 'newpost.html', context)


def error_404(request):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'500.html', data)