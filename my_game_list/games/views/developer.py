"""This module contains the viewsets for the Developer model."""
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import DeveloperFilterSet
from my_game_list.games.models import Developer
from my_game_list.games.serializers import DeveloperSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class DeveloperViewSet(ModelViewSet[Developer]):
    """A ViewSet for the Developer model."""

    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = DeveloperFilterSet
