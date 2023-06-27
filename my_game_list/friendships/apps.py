"""This module contains the configuration for the friendships application."""
from django.apps import AppConfig


class FriendshipConfig(AppConfig):
    """Configuration for the friendship application."""

    default_auto_field = "django.db.models.BigAutoField"  # type: ignore[assignment]
    name = "my_game_list.friendships"
