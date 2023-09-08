"""This module contains the viewsets for the GameList model."""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GameListFilterSet
from my_game_list.games.models import GameList
from my_game_list.games.serializers import GameListSerializer


class GameListViewSet(ModelViewSet[GameList]):
    """A ViewSet for the GameList model."""

    queryset = GameList.objects.all()
    serializer_class = GameListSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameListFilterSet
