"""This module contains the viewsets for the GameReview model."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import GameReview
from my_game_list.games.serializers import GameReviewSerializer


class GameReviewViewSet(ModelViewSet[GameReview]):
    """A ViewSet for the GameReview model."""

    queryset = GameReview.objects.all()
    serializer_class = GameReviewSerializer
    permission_classes = (IsAuthenticated,)
