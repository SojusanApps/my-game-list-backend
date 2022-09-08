from django.urls import include, path
from rest_framework import routers

from my_game_list.users.views import UserViewSet

app_name = "users"

router = routers.SimpleRouter()
router.register("user", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
