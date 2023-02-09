from rest_framework import serializers

from my_game_list.games.models import GameFollow


class GameFollowSerializer(serializers.ModelSerializer):
    """A serializer for the game follow model."""

    class Meta:
        model = GameFollow
        fields = ("id", "creation_time", "game", "user")
