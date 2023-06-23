"""This module contains the viewsets for the Publisher model."""
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import Publisher
from my_game_list.games.serializers import PublisherSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class PublisherViewSet(ModelViewSet):
    """A ViewSet for the Publisher model."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)
