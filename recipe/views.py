from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from .models import Recipe
from .forms import CreateRecipeForm, EditRecipeForm
# from django.core.mail import send_mail
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
        author = self.request.user.author
        return Recipe.objects.filter(author=author)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = "recipe/create_recipe.html"
    form_class = CreateRecipeForm

    def get_success_url(self):
        return reverse("recipe:recipe-list")

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.title = self.request.user.title
        recipe.author = self.request.user.author
        recipe.save()
        return super(RecipeCreateView, self).form_valid(form)


class RecipeEditView(LoginRequiredMixin, UpdateView):
    template_name = "recipe/edit-recipe.html"
    queryset = Recipe.objects.all()
    form_class = EditRecipeForm
    context_object_name = "recipe"

    def get_success_url(self):
        return reverse("recipe:recipe-list")

    def get_queryset(self):
        author = self.request.user.author
        return Recipe.objects.filter(author=author)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "recipe/delete-recipe.html"
    context_object_name = "recipe"

    def get_success_url(self):
        return reverse("recipe:recipe-list")

    def get_queryset(self):
        author = self.request.user.author
        return Recipe.objects.filter(author=author)


class Recipe_detail_view(View):
    def saved_recipe(self, request, recipe_id):
        saved_recipes = request.session.get("saved_recipes")
        if saved_recipes is not None:
            is_saved_for_later = recipe_id in saved_recipes
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        recipe = Recipe.objects.get(slug=slug)
        print(slug)
        context = {
            "recipe": recipe,
            "recipe_tags": recipe.tags.all(),
            "recipe_form": CreateRecipeForm(),
            # "favorite": recipe.favorite.all().order_by("-id"),
            "saved_for_later": self.saved_recipe(request, recipe.id)
        }
        return render(request, "recipe/recipe_detail.html", context)

    def post(self, request, slug):
        recipe_form = CreateRecipeForm(request.POST)
        recipe = Recipe.objects.get(slug=slug)

        if recipe_form.is_valid():
            new_recipe = recipe_form.save(commit=False)
            new_recipe.post = recipe
            new_recipe.save()

            return HttpResponseRedirect(reverse("recipe-detail", args=[slug]))       
        context = {
            "recipe": recipe,
            "recipe_tags": recipe.tags.all(),
            "recipe_form": recipe_form,
            # "favorite": recipe.favorite.all().order_by("-id")
        }
        return render(request, "recipe/recipe_detail.html", context)


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


# def edit_recipe_view(request, slug):
#     recipe = Recipe.objects.get(slug=slug)
#     form = EditRecipeForm(instance=recipe)
#     if request.method == "POST":
#         form = EditRecipeForm(request.POST, instance=recipe)
#         if form.is_valid():
#             form.save()
#             return redirect("/recipe")
#     context = {
#         "form": form,
#         "recipe": recipe
#     }
#     return render(request, "recipe/edit_recipe.html", context)


# def delete_recipe_view(request, slug):
#     recipe = Recipe.objects.get(slug=slug)
#     recipe.delete()
#     return redirect("/recipe")
