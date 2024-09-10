"""This module contains the viewsets for the GameList model."""

from typing import Self

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GameListFilterSet
from my_game_list.games.models import GameList
from my_game_list.games.serializers import GameListCreateSerializer, GameListSerializer


class GameListViewSet(ModelViewSet[GameList]):
    """A ViewSet for the GameList model."""

    queryset = GameList.objects.all()
    serializer_class = GameListSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameListFilterSet

    def get_serializer_class(self: Self) -> type[GameListCreateSerializer] | type[GameListSerializer]:
        """Get the serializer class for the Game model."""
        return (
            GameListCreateSerializer
            if self.action
            in [
                "create",
                "update",
                "partial_update",
            ]
            else GameListSerializer
        )
