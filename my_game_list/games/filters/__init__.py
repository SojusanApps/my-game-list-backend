"""This package contains all the filters used by the games application."""

from my_game_list.games.filters.company import CompanyFilterSet
from my_game_list.games.filters.game import GameFilterSet
from my_game_list.games.filters.game_follow import GameFollowFilterSet
from my_game_list.games.filters.game_list import GameListFilterSet
from my_game_list.games.filters.game_review import GameReviewFilterSet
from my_game_list.games.filters.genre import GenreFilterSet
from my_game_list.games.filters.platform import PlatformFilterSet

__all__ = [
    "CompanyFilterSet",
    "GameFilterSet",
    "GameFollowFilterSet",
    "GameListFilterSet",
    "GameReviewFilterSet",
    "GenreFilterSet",
    "PlatformFilterSet",
]
