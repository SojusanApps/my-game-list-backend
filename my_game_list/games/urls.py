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
router.register("developers", DeveloperViewSet, basename="developers")
router.register("game-follows", GameFollowViewSet, basename="game_follows")
router.register("game-lists", GameListViewSet, basename="game_lists")
router.register("game-reviews", GameReviewViewSet, basename="game-reviews")
router.register("games", GameViewSet, basename="games")
router.register("genres", GenreViewSet, basename="genres")
router.register("platforms", PlatformViewSet, basename="platforms")
router.register("publishers", PublisherViewSet, basename="publishers")

urlpatterns = [
    path("", include(router.urls)),
]
