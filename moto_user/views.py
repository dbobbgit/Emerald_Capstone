from recipe.models import Recipe
from post.models import Post
from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import MotoUser
from .forms import EditProfileForm

# Create your views here.


def MotoUserView(request, user_id: int):

    profile = MotoUser.objects.get(id=user_id)
    return render(request, 'profile.html', {"profile": profile})


def EditProfileView(request, user_id: int):
    ''' CAITLIN: ALLOWS USER TO EDIT THEIR PROFILE WITH FIELDS 
    PREVIOUSLY ENTERED INFO. ONCE USER SAVES INFO, AS OF 7/10 COMMIT 
    THEY ARE REROUTED TO HOMEPAGE ON WHICH AN HREF HAS BEEN ADDED AROUND
    THE USER'S USERNAME TO PROVIDE A LINK TO THEIR PROFILE'''

    current_profile = MotoUser.objects.get(id=user_id)

    if request.user.is_staff or request.user.is_authenticated:
        if request.method == "POST":
            form = EditProfileForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                current_profile.display_name = data['display_name']
                current_profile.bio = data['bio']
                current_profile.bike = data['bike']
                current_profile.riding_style = data['riding_style']
                current_profile.riding_level = data['riding_level']
                current_profile.avatar = data['avatar']
                current_profile.save()
            return HttpResponseRedirect(reverse("home"))

        form = EditProfileForm(initial={
            'avatar': current_profile.avatar,
            'display_name': current_profile.display_name,
            'bio': current_profile.bio,
            'bike': current_profile.bike,
            'riding_style': current_profile.riding_style,
            'riding_level': current_profile.riding_level
        })

        return render(request, "edit_profile.html", {"form": form})

    return HttpResponseRedirect(reverse("home"))


def Add_Favorite_Recipe(request, recipe_pk: int):
    current_user = Recipe.objects.filter(author=request.user).first()

    if current_user:
        recipe = Recipe.objects.get(id=recipe_pk)
        current_user.favorite_recipes.add(recipe)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Remove_Favorite_Recipe(request, recipe_pk: int):
    current_user = Recipe.objects.get(author=request.user)
    if current_user:
        recipe = Recipe.objects.get(id=recipe_pk)
        current_user.favorite_recipes.remove(recipe)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Add_Favorite_Post(request, post_id: str):
    current_user = request.user
    if current_user:
        post = Post.objects.get(id=post_id)
        current_user.favorite_posts.add(post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Remove_Favorite_Post(request, post_id: str):
    current_user = request.user
    if current_user:
        post = Post.objects.get(id=post_id)
        current_user.favorite_posts.remove(post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Follow_View(request, user_id: int):
    following = MotoUser.objects.get(id=user_id)
    if request.user.is_authenticated:
        if request.user.following.filter(id=user_id).exists() is False:
            request.user.following.add(following)
            following.save()
        count = request.user.following.all().count()
        if count is None:
            count = 0
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', {'count': count}))


def Unfollow_View(request, user_id: int):
    following = MotoUser.objects.get(id=user_id)
    if request.user.is_authenticated:
        if request.user.following.filter(id=user_id).exists():
            request.user.following.remove(following)
            following.save()
        count = request.user.following.all().count()
        if count is None:
            count = 0
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', {'count': count}))


def Following_View(request, user_id: int):
    following = request.user.following.exclude(following=user_id)
    return render(request, 'following.html', {'following': following})
