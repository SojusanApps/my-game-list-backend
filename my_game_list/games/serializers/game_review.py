"""This module contains the serializers for the GameReview model."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_game_list.games.models import GameReview
from my_game_list.users.serializers import UserSerializer

User = get_user_model()


class GameReviewSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for the game review model."""

    user = UserSerializer()

    class Meta:
        """Meta data for the game review serializer."""

        model = GameReview
        fields = ("id", "score", "created_at", "review", "game", "user")


class GameReviewCreateSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for creating the game review model."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="id",
    )

    class Meta:
        """Meta data for the game review create serializer."""

        model = GameReview
        fields = ("id", "score", "created_at", "review", "game", "user")
