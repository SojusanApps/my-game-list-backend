from django.urls import include, path
from rest_framework import routers

from my_game_list.games.views import (
    DeveloperViewSet,
    GameFollowViewSet,
    GameListViewSet,
    GameReviewViewSet,
    GameViewSet,
    GenreViewSet,
    PlatformViewSet,
    PublisherViewSet,
)

app_name = "games"

router = routers.SimpleRouter()
router.register("developer", DeveloperViewSet, basename="developers")
router.register("game-follow", GameFollowViewSet, basename="game_follows")
router.register("game-list", GameListViewSet, basename="game_lists")
router.register("game-review", GameReviewViewSet, basename="game-reviews")
router.register("game", GameViewSet, basename="games")
router.register("genre", GenreViewSet, basename="genres")
router.register("platform", PlatformViewSet, basename="platforms")
router.register("publisher", PublisherViewSet, basename="publishers")

urlpatterns = [
    path("", include(router.urls)),
]
