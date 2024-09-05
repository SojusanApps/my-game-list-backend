"""This module contains the viewsets for the Publisher model."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import PublisherFilterSet
from my_game_list.games.models import Publisher
from my_game_list.games.serializers import PublisherSerializer, PublisherSimpleNameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class PublisherViewSet(ModelViewSet[Publisher]):
    """A ViewSet for the Publisher model."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PublisherFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Publisher model."""
        data = Publisher.objects.all().order_by("name")
        serializer = PublisherSimpleNameSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
