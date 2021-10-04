from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

api_patterns = [
    path('favorites/', views.AddToFavorites.as_view(), name='favorites'),
    path(
        'favorites/<int:pk>/',
        views.RemoveFromFavorites.as_view(),
        name='remove_favorites'),
    path('subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path(
        'subscribe/<int:pk>/',
        views.UnSubscribe.as_view(),
        name='unsubscribe'
    ),
    path('purchases/', views.AddPurchase.as_view(), name='add_purchase'),
    path(
        'purchases/<int:pk>/',
        views.RemovePurchase.as_view(),
        name='remove_purchase'
    ),
    path('products', views.GetProducts.as_view()),
]

urlpatterns = [
    path('', include(format_suffix_patterns(api_patterns))),
]
