"""This module contains the configuration for user application."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the users application."""

    default_auto_field = "django.db.models.BigAutoField"  # type: ignore[assignment]
    name = "my_game_list.users"
