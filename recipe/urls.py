from django.urls import path
from .views import IndexView, FavoritesView, ProfileView, RecipeDetailView, MyFollowView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('recipes/<int:pk>', RecipeDetailView.as_view(), name='recipe'),
    path('myfollow/', MyFollowView.as_view(), name='myfollow')
]
