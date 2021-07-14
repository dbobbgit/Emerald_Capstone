from django.shortcuts import render, HttpResponseRedirect, reverse
# from django.views.generic import ListView
from django.views import View
from .models import Recipe
from .forms import CreateRecipeForm


# Create your views here.
# class Recipe_List_View(ListView):
#     template_name = "recipe/recipe_list.html"
#     model = Recipe
#     ordering = ["-date"]
#     context_object_name = "recipes"

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         data = queryset[:10]
#         return data

def Recipe_List_View(request):
    recipes = Recipe.objects.all().order_by("-date")[:10]
    return render(request, 'recipe/recipe_list.html', {
        "recipes": recipes,
    })



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
            "favorite": recipe.favorite.all().order_by("-id"),
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
            "favorite": recipe.favorite.all().order_by("-id")
        }
        return render(request, "recipe/recipe_detail.html", context)
