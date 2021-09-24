from django.urls import path
from .views import IndexView, FavoritesView, ProfileView, RecipeDetailView, MyFollowView, create_recipe, edit_recipe

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('recipes/<str:username>/<int:pk>/', RecipeDetailView.as_view(), name='recipe'),
    path('recipes/<str:username>/<int:pk>/edit/', edit_recipe, name='edit_recipe'),
    path('recipes/<str:username>/<int:pk>/delete/', edit_recipe, name='delete_recipe'),
    path('create/', create_recipe, name='create_recipe'),
    path('myfollow/', MyFollowView.as_view(), name='myfollow')
]
