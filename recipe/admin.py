from django.contrib import admin

from .models import (Favorites, Follow, Ingredient, OrderList, Product, Recipe,
                     Tag)


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    empty_value_display = '-пусто-'
    list_filter = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('pk', 'title', 'author')
    empty_value_display = '-пусто-'
    list_filter = ('title', 'author', 'tag')
    readonly_fields = ('favorite_count',)

    def favorite_count(self, obj):
        return obj.favorites.count()

    favorite_count.short_description = 'Добавлений в избранное'


admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Favorites)
admin.site.register(OrderList)
