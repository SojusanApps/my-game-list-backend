"""This module contains the view for api version."""

from collections.abc import Iterable, Mapping
from typing import Any, Self

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from my_game_list import __version__


class ApiVersion(APIView):
    """Endpoint for the version of the application."""

    permission_classes = (AllowAny,)

    def get(self: Self, *args: Iterable[Any], **kwargs: Mapping[str, Any]) -> Response:  # noqa: ARG002
        """GET method for the version of the application."""
        version = ".".join(map(str, __version__))
        return Response(version)
