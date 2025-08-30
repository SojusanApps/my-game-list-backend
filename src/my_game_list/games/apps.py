"""This module contains the configuration for the game application."""

from django.apps import AppConfig


class GamesConfig(AppConfig):
    """Configuration for the games application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "my_game_list.games"
