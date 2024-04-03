"""This module contains the serializers for the GameList model."""
import base64
from typing import Any, Self

from rest_framework import serializers

from my_game_list.games.models import GameList


class GameListSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list model."""

    status = serializers.CharField(source="get_status_display", read_only=True)
    title = serializers.CharField(source="game.title", read_only=True)
    game_cover_image = serializers.CharField(source="game.cover_image", read_only=True)

    class Meta:
        """Meta data for the game list serializer."""

        model = GameList
        fields = (
            "id",
            "status",
            "score",
            "created_at",
            "last_modified_at",
            "title",
            "game_cover_image",
            "user",
        )

    def to_representation(self: Self, instance: GameList) -> dict[str, Any]:
        """Object instance -> Dict of primitive datatypes."""
        representation = super().to_representation(instance)
        # Convert binary data to base64 encoded string
        representation["game_cover_image"] = base64.b64encode(instance.game.cover_image).decode("utf-8")
        return representation


class GameListCreateSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list create model."""

    class Meta:
        """Meta data for the game list create serializer."""

        model = GameList
        fields = (
            "id",
            "status",
            "score",
            "created_at",
            "last_modified_at",
            "game",
            "user",
        )
