from rest_framework import serializers

from my_game_list.games.models import GameReview


class GameReviewSerializer(serializers.ModelSerializer):
    """A serializer for the game review model."""

    class Meta:
        model = GameReview
        fields = ("id", "score", "creation_time", "review", "game", "user")
