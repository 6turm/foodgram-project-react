from django.contrib import admin
from .models import (
    Product, Recipe, Ingredient, Tag, Follow, Favorites, OrderList
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    empty_value_display = '-пусто-'
    list_filter = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    empty_value_display = '-пусто-'
    list_filter = ('title', 'author', 'tag')
    readonly_fields = ('favorite_count',)
    # fields = super().fields() + ('favorite_count')
    # list_filter = UserAdmin.list_filter + ('username', 'email')

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
