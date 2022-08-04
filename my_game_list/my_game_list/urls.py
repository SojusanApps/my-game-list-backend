from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from my_game_list.my_game_list.views import ApiVersion


urlpatterns = [
    path("admin/", admin.site.urls),
    path("version/", ApiVersion.as_view(), name="api-version")
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r"^rosetta/", include("rosetta.urls"))
    ]
