from django.contrib import admin
from .models import Recipe, Tag

# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_filter = ('title',)
    # prepopulated_fields = {'id': ('title', )}


admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(Author)
admin.site.register(Tag)
