"""This module contains the serializers for the GameList model."""
from rest_framework import serializers

from my_game_list.games.models import GameList


class GameListSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list model."""

    status_full_name = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        """Meta data for the game list serializer."""

        model = GameList
        fields = ("id", "status", "status_full_name", "created_at", "last_modified_at", "game", "user")
