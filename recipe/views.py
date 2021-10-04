import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.expressions import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import RecipeForm
from .models import Follow, OrderList, Recipe, Tag, User
from .utils import (get_ingredients_from_recipe, get_ingredients_from_request,
                    save_recipe)


class IndexView(ListView):
    queryset = Recipe.objects.all()
    paginate_by = 6
    template_name = 'index.html'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        queryset = super().get_queryset()
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if self.request.user.is_authenticated:
            queryset = queryset.annotate_favorites(
                user_id=self.request.user.id
            )
            queryset = queryset.annotate(is_purchase=Exists(
                OrderList.objects.filter(
                    user=self.request.user, recipe_id=OuterRef('pk'))
            ))
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['tags'] = Tag.objects.all()
        return context


class FavoritesView(LoginRequiredMixin, ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'recipe_list'
    paginate_by = 6
    template_name = 'favorites.html'

    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        queryset = super().get_queryset()
        queryset = queryset.filter(favorites__user=self.request.user)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        queryset = queryset.annotate(is_purchase=Exists(
            OrderList.objects.filter(
                user=self.request.user, recipe_id=OuterRef('pk'))
        ))
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['tags'] = Tag.objects.all()
        return context


class MyFollowView(LoginRequiredMixin, ListView):
    queryset = User.objects.prefetch_related('recipes')
    template_name = 'myFollow.html'
    context_object_name = 'author_list'
    paginate_by = 6

    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(following__user=self.request.user)
        queryset = queryset.annotate(is_follow=Exists(
            Follow.objects.filter(
                user=self.request.user, author_id=OuterRef('pk'))
        ))
        queryset = queryset.annotate(is_purchase=Exists(
            OrderList.objects.filter(
                user=self.request.user, recipe_id=OuterRef('pk'))
        ))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(ListView):
    context_object_name = 'recipe_list'
    paginate_by = 6
    template_name = 'profile.html'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = author.recipes.all()
        if self.request.user.is_authenticated:
            queryset = queryset.annotate_favorites(
                user_id=self.request.user.id
            )
            queryset = queryset.annotate(is_purchase=Exists(
                OrderList.objects.filter(
                    user=self.request.user, recipe_id=OuterRef('pk'))
            ))
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author'] = author
        if self.request.user.is_authenticated:
            context['is_follow'] = Follow.objects.filter(
                user=self.request.user, author=author).exists()
        context['tags'] = Tag.objects.all()
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object.author
        recipe = self.object
        if self.request.user.is_authenticated:
            context['is_follow'] = Follow.objects.filter(
                user=self.request.user, author=author).exists()
            context['is_purchase'] = OrderList.objects.filter(
                user=self.request.user, recipe=recipe).exists()
        return context


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'purchases'
    template_name = 'shop_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(order_list__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def dounload_purchases(request):
    recipes = Recipe.objects.filter(order_list__user=request.user)
    purchase_list = recipes.values_list(
        'ingredients__product__id',
        'ingredients__product__title',
        'ingredients__amount',
        'ingredients__product__dimension'
    )

    purchase_dict = {x[0]: [x[1], 0, x[3]] for x in purchase_list}

    for ing in purchase_list:
        purchase_dict[ing[0]][1] += ing[2]

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shop_list.txt"'
    writer = csv.writer(response)
    for ing in purchase_dict.values():
        writer.writerow([f'{ing[0]} ({ing[2]}) — {ing[1]}'])

    return response


@login_required
def create_recipe(request):
    ingredients = {}

    if request.method == 'POST':
        ingredients = get_ingredients_from_request(request)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        ingredients=ingredients
    )

    if form.is_valid():
        recipe = save_recipe(request, form, ingredients)
        return redirect(
            'recipe', pk=recipe.id, username=recipe.author.username
        )

    context = {'form': form, 'ingredients': ingredients}
    # ингридиенты передаются для повторного отображения в случае ошибок
    # при отправке формы
    return render(request, 'recipe_create.html', context)


@login_required
def edit_recipe(request, username, pk):
    recipe = get_object_or_404(Recipe, author__username=username, id=pk)
    if request.user != recipe.author:
        return redirect('recipe', pk=pk, username=username)

    if request.method == 'POST':
        ingredients = get_ingredients_from_request(request)
    else:
        ingredients = get_ingredients_from_recipe(recipe)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None,
        instance=recipe, ingredients=ingredients
    )

    if form.is_valid():
        recipe.ingredients.all().delete()
        recipe = save_recipe(request, form, ingredients)
        return redirect(
            'recipe', pk=recipe.id, username=recipe.author.username
        )

    context = {'form': form, 'ingredients': ingredients}
    # ингридиенты передаются для повторного отображения в случае ошибок
    # при отправке формы
    return render(request, 'recipe_create.html', context)


@login_required
def delete_recipe(request, username, pk):
    recipe = get_object_or_404(Recipe, author__username=username, id=pk)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')
