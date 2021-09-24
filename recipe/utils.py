from recipe.models import Ingredient, Product
from django.db import transaction
from django.shortcuts import get_object_or_404
from decimal import *


def get_ingredients_from_request(request):
    '''Получаем ингридиенты из результата работы js'''
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = [post[f'valueIngredient_{num}'], post[f'unitsIngredient_{num}']]
    return ingredients


def get_ingredients_from_recipe(recipe):
    '''Получаем ингридиенты из переданного рецепта в начале редактирования'''
    ing_objects = recipe.ingredients.all()
    ingredients = {}
    for ing in ing_objects:
        ingredients[ing.product.title] = [ing.amount, ing.product.title]
    return ingredients


def save_recipe(request, form, ingredients):
    '''Сохраняем рецепт создавая ингредиенты'''
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        objs = []
        for name, params in ingredients.items():
            product = get_object_or_404(Product, title=name)
            objs.append(Ingredient(product=product, recipe=recipe, amount=Decimal(params[0].replace(',', '.'))))

        Ingredient.objects.bulk_create(objs)
        form.save_m2m()
        return recipe
