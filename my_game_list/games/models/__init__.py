"""This package contains all the models used by the games application."""

from my_game_list.games.models.company import Company
from my_game_list.games.models.game import Game
from my_game_list.games.models.game_follow import GameFollow
from my_game_list.games.models.game_list import GameList, GameListStatus
from my_game_list.games.models.game_review import GameReview
from my_game_list.games.models.genre import Genre
from my_game_list.games.models.platform import Platform

__all__ = [
    "Company",
    "Game",
    "GameFollow",
    "GameList",
    "GameListStatus",
    "GameReview",
    "Genre",
    "Platform",
]
