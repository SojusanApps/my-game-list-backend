"""This module contains the serializers for the GameReview model."""
from typing import Self

from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_game_list.games.models import GameReview
from my_game_list.users.serializers.user import UserSerializer

User = get_user_model()


class GameReviewSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for the game review model."""

    user = UserSerializer()
    score = serializers.SerializerMethodField()

    class Meta:
        """Meta data for the game review serializer."""

        model = GameReview
        fields = ("id", "score", "created_at", "review", "game", "user")

    def get_score(self: Self, instance: GameReview) -> int | None:
        """Get user score for the this game."""
        game_list_instance = instance.user.game_lists.filter(game__id=instance.game.id).first()
        if game_list_instance:
            return game_list_instance.score
        return None


class GameReviewCreateSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for creating the game review model."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="id",
    )

    class Meta:
        """Meta data for the game review create serializer."""

        model = GameReview
        fields = ("id", "created_at", "review", "game", "user")
