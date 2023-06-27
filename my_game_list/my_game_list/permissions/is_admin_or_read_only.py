"""This module contains the custom permission class."""
from typing import Self

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """The request is authenticated as a admin user, or is a read-only request."""

    def has_permission(self: Self, request: Request, view: APIView) -> bool:
        """Check if the request has permission."""
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))
