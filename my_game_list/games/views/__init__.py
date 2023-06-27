"""This package contains viewsets for the games application."""
from my_game_list.games.views.developer import DeveloperViewSet
from my_game_list.games.views.game import GameViewSet
from my_game_list.games.views.game_follow import GameFollowViewSet
from my_game_list.games.views.game_list import GameListViewSet
from my_game_list.games.views.game_review import GameReviewViewSet
from my_game_list.games.views.genre import GenreViewSet
from my_game_list.games.views.platform import PlatformViewSet
from my_game_list.games.views.publisher import PublisherViewSet

__all__ = [
    "DeveloperViewSet",
    "GameViewSet",
    "GameFollowViewSet",
    "GameListViewSet",
    "GameReviewViewSet",
    "GenreViewSet",
    "PlatformViewSet",
    "PublisherViewSet",
]
