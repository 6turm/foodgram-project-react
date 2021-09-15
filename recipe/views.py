from django.db.models.expressions import Exists, OuterRef
from django.db.models.query import Prefetch, QuerySet
from django.shortcuts import get_object_or_404
from .models import Follow, Recipe, User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'recipe_list'
    paginate_by = 6
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        return queryset


class FavoritesView(LoginRequiredMixin, ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'recipe_list'
    paginate_by = 6
    template_name = 'favorites.html'

    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        queryset = queryset.filter(favorites__user=self.request.user)
        return queryset


class MyFollowView(LoginRequiredMixin, ListView):
    queryset = User.objects.prefetch_related('recipes')
    template_name = 'myFollow.html'
    context_object_name = 'author_list'
    paginate_by = 3

    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(following__user=self.request.user)
        queryset = queryset.annotate(is_follow=Exists(
            Follow.objects.filter(
                user_id=self.request.user.id, author_id=OuterRef('pk'))
        ))
        print('@@@ queryset of MyFollow: ', queryset)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('@@@ context of MyFollow: ', context)
        return context


class ProfileView(ListView):
    context_object_name = 'recipe_list'
    paginate_by = 6
    template_name = 'profile.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        qureyset = author.recipes.all()
        qureyset = qureyset.annotate_favorites(user_id=self.request.user.id)
        return qureyset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author'] = author
        context['is_follow'] = Follow.objects.filter(
            user_id=self.request.user.id, author_id=author.id).exists()
        print('Context ProfileView: ',context )
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
        author_id = super().get_object().author.id
        context['is_follow'] = Follow.objects.filter(
            user_id=self.request.user.id, author_id=author_id
        ).exists()
        print('Context RecipeDetailView: ',context )
        return context

