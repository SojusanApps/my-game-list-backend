"""This module contains the url configuration for the application."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from my_game_list.my_game_list.prometheus import custom_export_to_django_view
from my_game_list.my_game_list.views import ApiVersion

urlpatterns = [
    path("admin/", admin.site.urls),
    path("prometheus/metrics", custom_export_to_django_view, name="prometheus-django-metrics"),
    path("version/", ApiVersion.as_view(), name="api-version"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/", include("my_game_list.users.urls")),
    path("api/game/", include("my_game_list.games.urls")),
    path("api/friendship/", include("my_game_list.friendships.urls")),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

# To work with files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
