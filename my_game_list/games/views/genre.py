"""This module contains the viewsets for the Genre model."""
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import Genre
from my_game_list.games.serializers import GenreSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class GenreViewSet(ModelViewSet):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
