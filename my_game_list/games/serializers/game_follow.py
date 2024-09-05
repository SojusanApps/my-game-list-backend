"""This module contains the serializers for the GameFollow model."""

from rest_framework import serializers

from my_game_list.games.models import GameFollow


class GameFollowSerializer(serializers.ModelSerializer[GameFollow]):
    """A serializer for the game follow model."""

    class Meta:
        """Meta data for game follow serializer."""

        model = GameFollow
        fields = ("id", "created_at", "game", "user")
