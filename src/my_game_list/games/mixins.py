"""
This module contains the mixins for the game related ViewSets.

The mixins are used to add custom functionality to the ViewSets.
"""

from typing import TYPE_CHECKING, Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


class DictionaryAllValuesMixin:
    """A mixin for ViewSets that allows to get all values of the model."""

    @action(detail=False, methods=("get",), url_path="all-values", pagination_class=None)
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Publisher model."""
        data = self.get_queryset().order_by("name")  # type: ignore[attr-defined]
        serializer = self.get_serializer(data, many=True)  # type: ignore[attr-defined]

        return Response(serializer.data, status=status.HTTP_200_OK)
