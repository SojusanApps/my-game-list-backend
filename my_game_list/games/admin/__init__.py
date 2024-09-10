"""This package contains all the admin models used by the games application."""

from my_game_list.games.admin.company import CompanyAdmin
from my_game_list.games.admin.game import GameAdmin
from my_game_list.games.admin.game_follow import GameFollowAdmin
from my_game_list.games.admin.game_list import GameListAdmin
from my_game_list.games.admin.game_review import GameReviewAdmin
from my_game_list.games.admin.genre import GenreAdmin
from my_game_list.games.admin.platform import PlatformAdmin

__all__ = [
    "CompanyAdmin",
    "GameAdmin",
    "GameFollowAdmin",
    "GameListAdmin",
    "GameReviewAdmin",
    "GenreAdmin",
    "PlatformAdmin",
]
