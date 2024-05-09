"""This module contains the viewsets for the Game model."""
from typing import Self

from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GameFilterSet
from my_game_list.games.models import Game
from my_game_list.games.serializers import GameCreateSerializer, GameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class GameViewSet(ModelViewSet[Game]):
    """A ViewSet for the Game model."""

    queryset = Game.objects.all().prefetch_related("game_lists").with_rank_position().with_popularity()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameFilterSet
    ordering_fields = ("release_date",)
    ordering = ("release_date",)

    def get_serializer_class(self: Self) -> type[GameCreateSerializer] | type[GameSerializer]:
        """Get the serializer class for the Game model."""
        return GameCreateSerializer if self.action in ["create", "update", "partial_update"] else GameSerializer
