"""This module contains the viewsets for the Platform model."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import PlatformFilterSet
from my_game_list.games.models import Platform
from my_game_list.games.serializers import PlatformSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class PlatformViewSet(ModelViewSet[Platform]):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlatformFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Publisher model."""
        data = Platform.objects.all().order_by("name")
        serializer = PlatformSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
