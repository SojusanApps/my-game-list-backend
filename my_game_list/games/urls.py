"""This module contains the urls for the game application."""

from django.urls import include, path
from rest_framework import routers

from my_game_list.games.views import (
    CompanyViewSet,
    GameFollowViewSet,
    GameListViewSet,
    GameMediaViewSet,
    GameReviewViewSet,
    GameViewSet,
    GenreViewSet,
    PlatformViewSet,
)

app_name = "games"

router = routers.SimpleRouter()
router.register("companies", CompanyViewSet, basename="companies")
router.register("game-follows", GameFollowViewSet, basename="game-follows")
router.register("game-lists", GameListViewSet, basename="game-lists")
router.register("game-reviews", GameReviewViewSet, basename="game-reviews")
router.register("games", GameViewSet, basename="games")
router.register("genres", GenreViewSet, basename="genres")
router.register("platforms", PlatformViewSet, basename="platforms")
router.register("game-medias", GameMediaViewSet, basename="game-medias")

urlpatterns = [
    path("", include(router.urls)),
]
