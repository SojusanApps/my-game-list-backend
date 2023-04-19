from rest_framework import serializers

from my_game_list.games.models import GameList


class GameListSerializer(serializers.ModelSerializer):
    """A serializer for the game list model."""

    class Meta:
        """Meta data for the game list serializer."""

        model = GameList
        fields = ("id", "status", "created_at", "last_modified_at", "game", "user")
