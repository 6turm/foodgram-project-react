from django.urls import path
from .views import IndexView, FavoritesView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favorites/', FavoritesView.as_view(), name='favorites')
    # path('')
]
