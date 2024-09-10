"""This package contains viewsets for the games application."""

from my_game_list.games.views.company import CompanyViewSet
from my_game_list.games.views.game import GameViewSet
from my_game_list.games.views.game_follow import GameFollowViewSet
from my_game_list.games.views.game_list import GameListViewSet
from my_game_list.games.views.game_review import GameReviewViewSet
from my_game_list.games.views.genre import GenreViewSet
from my_game_list.games.views.platform import PlatformViewSet

__all__ = [
    "CompanyViewSet",
    "GameViewSet",
    "GameFollowViewSet",
    "GameListViewSet",
    "GameReviewViewSet",
    "GenreViewSet",
    "PlatformViewSet",
]
