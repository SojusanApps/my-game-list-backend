"""This module contains the viewsets for the Genre model."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import GenreFilterSet
from my_game_list.games.models import Genre
from my_game_list.games.serializers import GenreSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class GenreViewSet(ModelViewSet[Genre]):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GenreFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Publisher model."""
        data = Genre.objects.all().order_by("name")
        serializer = GenreSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
