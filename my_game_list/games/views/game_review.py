"""This module contains the viewsets for the GameReview model."""

from typing import Self

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GameReviewFilterSet
from my_game_list.games.models import GameReview
from my_game_list.games.serializers import GameReviewCreateSerializer, GameReviewSerializer


class GameReviewViewSet(ModelViewSet[GameReview]):
    """A ViewSet for the GameReview model."""

    queryset = GameReview.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = GameReviewFilterSet

    def get_serializer_class(self: Self) -> type[GameReviewCreateSerializer] | type[GameReviewSerializer]:
        """Get the serializer class for the Game model."""
        return (
            GameReviewCreateSerializer
            if self.action
            in [
                "create",
                "update",
                "partial_update",
            ]
            else GameReviewSerializer
        )
