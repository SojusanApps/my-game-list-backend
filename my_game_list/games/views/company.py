"""This module contains the viewsets for the Company model."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import CompanyFilterSet
from my_game_list.games.models import Company
from my_game_list.games.serializers import CompanySerializer, CompanySimpleNameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class CompanyViewSet(ModelViewSet[Company]):
    """A ViewSet for the Company model."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = CompanyFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Company model."""
        data = Company.objects.all().order_by("name")
        serializer = CompanySimpleNameSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
