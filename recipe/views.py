from django.shortcuts import get_object_or_404, render
from .models import Recipe, Favorites, User
from django.core.paginator import Paginator
from django.views.generic.list import ListView
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
        return context
