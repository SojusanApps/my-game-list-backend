"""This module contains the viewsets for the Developer model."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import DeveloperFilterSet
from my_game_list.games.models import Developer
from my_game_list.games.serializers import DeveloperSerializer, DeveloperSimpleNameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class DeveloperViewSet(ModelViewSet[Developer]):
    """A ViewSet for the Developer model."""

    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = DeveloperFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Developer model."""
        data = Developer.objects.all().order_by("name")
        serializer = DeveloperSimpleNameSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
