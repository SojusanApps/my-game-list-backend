"""This package contains all the serializers used by the games application."""

from my_game_list.games.serializers.developer import DeveloperSerializer, DeveloperSimpleNameSerializer
from my_game_list.games.serializers.game import GameCreateSerializer, GameSerializer
from my_game_list.games.serializers.game_follow import GameFollowSerializer
from my_game_list.games.serializers.game_list import GameListCreateSerializer, GameListSerializer
from my_game_list.games.serializers.game_review import GameReviewCreateSerializer, GameReviewSerializer
from my_game_list.games.serializers.genre import GenreSerializer
from my_game_list.games.serializers.platform import PlatformSerializer
from my_game_list.games.serializers.publisher import PublisherSerializer, PublisherSimpleNameSerializer

__all__ = [
    "DeveloperSerializer",
    "DeveloperSimpleNameSerializer",
    "GameCreateSerializer",
    "GameSerializer",
    "GameFollowSerializer",
    "GameListSerializer",
    "GameListCreateSerializer",
    "GameReviewCreateSerializer",
    "GameReviewSerializer",
    "GenreSerializer",
    "PlatformSerializer",
    "PublisherSerializer",
    "PublisherSimpleNameSerializer",
]
