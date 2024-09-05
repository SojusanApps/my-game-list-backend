"""This package contains all the filters used by the games application."""

from my_game_list.games.filters.developer import DeveloperFilterSet
from my_game_list.games.filters.game import GameFilterSet
from my_game_list.games.filters.game_follow import GameFollowFilterSet
from my_game_list.games.filters.game_list import GameListFilterSet
from my_game_list.games.filters.game_review import GameReviewFilterSet
from my_game_list.games.filters.genre import GenreFilterSet
from my_game_list.games.filters.platform import PlatformFilterSet
from my_game_list.games.filters.publisher import PublisherFilterSet

__all__ = [
    "DeveloperFilterSet",
    "GameFilterSet",
    "GameFollowFilterSet",
    "GameListFilterSet",
    "GameReviewFilterSet",
    "GenreFilterSet",
    "PlatformFilterSet",
    "PublisherFilterSet",
]
