from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from .models import Recipe, Tag
from .forms import RecipeForm
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
        author = self.request.user.pk
        return Recipe.objects.filter(author=author)


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
            author = data.get('author')
            image = data.get('image')
            # tags_form = data.get('tags')
            # tags_list = list(tags_form.split(','))
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
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("/recipe")
    context = {
        "form": form,
        "recipe": recipe
    }
    return render(request, "recipe/edit_recipe.html", context)


@login_required
def delete_recipe_view(request, pk):
    recipe = Recipe.objects.get(id=pk)
    recipe.delete()
    return redirect("/recipe")



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

# def create_Recipe_view(request, slug):
#     form = CreateRecipeForm()
#     if request.method == "POST":
#         form = CreateRecipeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/recipe")
#     context = {
#         "form": form
#     }
#     return render(request, "recipe/recipe-detail.html", context)




# def delete_recipe_view(request, pk):
#     recipe = Recipe.objects.get(id=pk)
#     recipe.delete()
#     return redirect('recipe:recipe-list')
