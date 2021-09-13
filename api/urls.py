from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

api_patterns = [
    path('favorites/', views.AddToFavorites.as_view(), name='favorites'),
    path(
        'favorites/<int:pk>/',
        views.RemoveFromFavorites.as_view(),
        name='remove_favorites'),
    path('subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path('subscribe/<int:pk>/', views.UnSubscribe.as_view(), name='unsubscribe'),
]

urlpatterns = [
    path('', include(format_suffix_patterns(api_patterns))),
]
