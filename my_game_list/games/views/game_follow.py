"""This module contains the viewsets for the GameFollow model."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GameFollowFilterSet
from my_game_list.games.models import GameFollow
from my_game_list.games.serializers import GameFollowSerializer


class GameFollowViewSet(ModelViewSet[GameFollow]):
    """A ViewSet for the GameFollow model."""

    queryset = GameFollow.objects.all()
    serializer_class = GameFollowSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameFollowFilterSet
