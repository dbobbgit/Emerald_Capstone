from django.contrib import admin
from .models import Recipe, Author, Tag

# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Author)
admin.site.register(Tag)
