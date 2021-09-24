from django.contrib.auth.decorators import login_required
from django.db.models.expressions import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from .models import Follow, OrderList, Recipe, User, Tag
from .forms import RecipeForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import get_ingredients_from_request, save_recipe, get_ingredients_from_recipe


class IndexView(ListView):
    queryset = Recipe.objects.all()
    paginate_by = 6
    template_name = 'index.html'

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        queryset = super().get_queryset()
        if tags:
            queryset = queryset.filter(tag__slug__in=tags).distinct()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        queryset = queryset.annotate(is_purchase=Exists(
            OrderList.objects.filter(
                user_id=self.request.user.id, recipe_id=OuterRef('pk'))
                )
            )
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
            queryset = queryset.filter(tag__slug__in=tags)
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
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
                user_id=self.request.user.id, author_id=OuterRef('pk'))
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
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        if tags:
            queryset = queryset.filter(tag__slug__in=tags)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author'] = author
        context['is_follow'] = Follow.objects.filter(
            user_id=self.request.user.id, author_id=author.id).exists()
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
        author_id = self.object.author.id
        recipe_id = self.object.pk
        context['is_follow'] = Follow.objects.filter(
            user_id=self.request.user.id, author_id=author_id
        ).exists()
        context['is_purchase'] = OrderList.objects.filter(
            user_id=self.request.user.id, recipe_id=recipe_id
        ).exists()
        print('@@@@ context', context)
        return context


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'purchases'
    # paginate_by = 6
    template_name = 'shop_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(order_list__user_id=self.request.user.id)
        print('@@@@ ', queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('@@@ context', context)
        return context


def dounload_purchases(request):
    pass


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
