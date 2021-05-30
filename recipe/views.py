from django.shortcuts import render
from .models import Recipe, Favorites
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

# def index(request):
#     recipe_list = Recipe.objects.all()  # select_related('имя связи') - для кэширования связанных объектов
#     # print(recipe_list)
#     # recipe_list = super().get_queryset()
#     paginator = Paginator(recipe_list, 6)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     return render(
#         request,
#         'index.html',
#         {'page': page, 'paginator': paginator}
#     )
