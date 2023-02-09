from rest_framework import serializers

from my_game_list.games.models import GameList


class GameListSerializer(serializers.ModelSerializer):
    """A serializer for the game list model."""

    class Meta:
        model = GameList
        fields = ("id", "status", "creation_time", "last_modified", "game", "user")
