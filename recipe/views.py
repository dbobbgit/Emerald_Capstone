from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, reverse, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Recipe, Tag
from .forms import RecipeForm, CommentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class RecipeListView(LoginRequiredMixin, ListView):
    template_name = "recipe/recipe_list.html"
    model = Recipe
    ordering = ["-date"]
    context_object_name = "recipes"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:10]
        return data

# def recipe_List_View(request):
#     recipes = Recipe.objects.all().order_by("-date")[:10]
#     return render(request, 'recipe/recipe_list.html', {
#         "recipes": recipes,
#     })


class RecipeDetailView(LoginRequiredMixin, DetailView):
    template_name = "recipe/recipe_detail.html"
    context_object_name = "recipe"

    def get_success_url(self):
        return reverse("recipe:recipe-list")

    def get_queryset(self):
        # author = self.request.user.pk
        # print(author)
        return Recipe.objects.all()
    # def get(self, request, pk):
    #     recipe_post = Recipe.objects.get(id=pk)

    #     context = {
    #         "recipe": recipe_post,
    #         "comment_form": CommentForm(),
    #         "comments": recipe_post.comments.all().order_by("-id"),
    #     }
    #     return render(request, "recipe/recipe_detail.html", context)

    # def post(self, request, pk):
    #     # author = request.user.display_name
    #     comment_form = CommentForm(request.POST)
    #     recipe_post = Recipe.objects.get(id=pk)

    #     if comment_form.is_valid():
    #         comment = comment_form.save(commit=False)
    #         comment.post = recipe_post
    #         comment.save()

    #         return HttpResponseRedirect(reverse("recipe-detail", args=[pk]))
        
    #     context = {
    #         "recipe": recipe_post,
    #         "comment_form": comment_form,
    #         "comments": recipe_post.comments.all().order_by("-id")
    #     }
    #     return render(request, "recipe/recipe_detail.html", context)


@login_required
def create_recipe_view(request):
    tags_list = []

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get("title")
            time_required = data.get('time_required')
            description = data.get('description')
            instruction = data.get('instruction')
            image = data.get('image')
            for tag in tags_list:
                tag, __ = Tag.objects.get_or_create(title=tag)
                tags_list.append(tag)
            recipe, __ = Recipe.objects.get_or_create(
                image=image,
                author=request.user,
                title=title,
                time_required=time_required,
                description=description,
                instruction=instruction
                )
            recipe.tags.set(tags_list)
            messages.success(request, 'Your recipe has been created!!')
            recipe.save()
            return redirect('recipe:recipe-list')
    else:
        form = RecipeForm()

    context = {
        'form': form,
    }
    
    return render(request, 'recipe/create_recipe.html', context)


@login_required
def edit_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    form = RecipeForm(instance=recipe)
    context = {
        "form": form,
        "recipe": recipe
    }
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data.get('title')
            recipe.description = data.get('description')
            recipe.time_required = data.get('time_required')
            recipe.instruction = data.get('instruction')
            recipe.image = data.get('image')
            messages.success(request, 'Recipe has been updated!!')
            recipe.save()
            return redirect("/recipe")

    form = RecipeForm(initial={
        'title': recipe.title,
        'description': recipe.description,
        'time_required': recipe.time_required,
        'instruction': recipe.instruction,
        'image': recipe.image,
    }            
    )
    return render(request, "recipe/edit_recipe.html", context)


@login_required
def delete_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    context = {'recipe': recipe}

    if request.method == "POST":
        recipe.delete()
        return redirect("/recipe")
    return render(request, "recipe/delete_recipe.html", context)


def comment_view(request, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
  
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = recipe
            comment.save()
            # data = form.cleaned_data
            # recipe.text = data.get('text')
            # recipe.author = data.get('author')
            # recipe.save()
          
            return redirect('recipe:recipe-detail', pk=recipe.pk)
    else:
        form = CommentForm()
    return render(request, 'recipe/add_comment.html', {'form': form, 'recipe': recipe})


# def comment_view(request, pk):
#     comment_form = CommentForm(request.POST)
#     recipe_post = Recipe.objectscts.get(id=pk)

#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.post = recipe_post
#         comment.save()

#         return HttpResponseRedirect(reverse("recipe-detail", args=[pk]))
    
#     context = {
#         "post": recipe_post,
#         "comment_form": comment_form,
#         "comments": recipe_post.comments.all().order_by("-id")
#     }
#     return render(request, "recipe/recipe_detail.html", context)

# class RecipeDeleteView(LoginRequiredMixin, DeleteView):
#     template_name = "recipe/delete_recipe.html"

#     def get_success_url(self):
#         return reverse("recipe:recipe-list")

#     def get_queryset(self):
#         author = self.request.user.pk
#         return Recipe.objects.filter(author=author)


class RecipeSavedView(View):
    def get(self, request):
        saved_recipes = request.session.get("saved_recipes")

        context = {}

        if saved_recipes is None or len(saved_recipes) == 0:
            context["recipes"] = []
            context["has_recipes"] = False
        else:
            recipes = Recipe.objects.filter(id__in=saved_recipes)
            context["recipes"] = recipes
            context["has_recipes"] = True

        return render(request, "recipe/saved_recipe.html", context)

    def post(self, request):
        saved_recipes = request.session.get("saved_recipes")

        if saved_recipes is None:
            saved_recipes = []

        recipe_id = int(request.POST["recipe_id"])
    
        if recipe_id not in saved_recipes:
            saved_recipes.append(recipe_id)
            request.session["saved_recipes"] = saved_recipes
        else:
            saved_recipes.remove(recipe_id)

        request.session["saved_recipes"] = saved_recipes
                
        return HttpResponseRedirect("recipe:recipe-list")