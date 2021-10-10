from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "foodgram.views.page_not_found"
handler500 = "foodgram.views.server_error"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('api/', include('api.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('recipe.urls')),
]


urlpatterns += [
    path(
        'about-author/', views.flatpage,
        {'url': '/about-author/'}, name='about_author'
    ),
    path(
        'about-spec/', views.flatpage,
        {'url': '/about-spec/'}, name='about_spec'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
