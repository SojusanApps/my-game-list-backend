from rest_framework import serializers

from my_game_list.games.models import GameReview


class GameReviewSerializer(serializers.ModelSerializer):
    """A serializer for the game review model."""

    class Meta:
        """Meta data for the game review serializer."""

        model = GameReview
        fields = ("id", "score", "created_at", "review", "game", "user")
