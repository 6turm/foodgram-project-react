from django.shortcuts import get_object_or_404
from .models import Follow, Recipe, User, Favorites
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


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate_favorites(user_id=self.request.user.id)
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     is_favorite = Favorites.objects.filter(
    #         user__username=self.request.user,
    #         recipe__id=self.object.id
    #     ).exists()
    #     context['is_favorite'] = is_favorite
    #     print(self.object.author, self.object.id)
    #     print(is_favorite)
    #     return context
