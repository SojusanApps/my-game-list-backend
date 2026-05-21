"""This module contains the viewsets for user related interactions."""

from typing import TYPE_CHECKING, Self

from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

if TYPE_CHECKING:
    from rest_framework.authentication import BaseAuthentication

from my_game_list.users.filters import UserFilterSet
from my_game_list.users.models import User as UserModel
from my_game_list.users.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserSerializer,
)

User: type[UserModel] = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description=(
            "List user accounts. Returns public user information for all users. "
            "Filter by username (partial match), gender, or active status."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact user ID.",
            ),
            OpenApiParameter(
                name="username",
                description="Filter by username. Case-insensitive partial match.",
            ),
            OpenApiParameter(
                name="gender",
                description=("Filter by gender. Can be specified multiple times to match several values."),
            ),
            OpenApiParameter(
                name="is_active",
                description="Filter by account active status. When true, return only active accounts.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description=(
            "Retrieve a user account by ID. "
            "The authenticated account owner receives additional private fields "
            "(e.g. email address) that are not visible to other users."
        ),
    ),
    create=extend_schema(
        description=(
            "Register a new user account. "
            "This endpoint is publicly accessible and requires no authentication. "
            "Provide a unique username, a valid email address, and a password meeting "
            "the site's complexity requirements."
        ),
    ),
)
class UserViewSet(GenericViewSet[UserModel], ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """ViewSet is responsible for creating, listing, and retrieving user information."""

    queryset = User.objects.all()
    filterset_class = UserFilterSet

    def get_serializer_class(
        self: Self,
    ) -> type[UserCreateSerializer | UserSerializer | UserDetailSerializer]:
        """Get the serializer class for the User model."""
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_authenticators(self: Self) -> list[BaseAuthentication]:
        """Get the authenticators for the actions."""
        action = getattr(self, "action", None)
        if action == "create":
            return []

        if action is None and self.request.method == "POST":
            return []

        return super().get_authenticators()

    def get_permissions(self: Self) -> list[BasePermission]:
        """Get the permissions for the actions."""
        permission_classes = (AllowAny,) if self.action == "create" else (IsAuthenticated,)
        return [permission() for permission in permission_classes]
