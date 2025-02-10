"""This module contains the viewsets for user related interactions."""

from typing import Self

from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from my_game_list.users.filters import UserFilterSet
from my_game_list.users.models import User as UserModel
from my_game_list.users.serializers import UserCreateSerializer, UserDetailSerializer, UserSerializer

User: type[UserModel] = get_user_model()


class UserViewSet(GenericViewSet[UserModel], ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """ViewSet is responsible for creating, listing, and retrieving user information."""

    queryset = User.objects.all()
    filterset_class = UserFilterSet

    def get_serializer_class(
        self: Self,
    ) -> type[UserCreateSerializer] | type[UserSerializer] | type[UserDetailSerializer]:
        """Get the serializer class for the User model."""
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self: Self) -> list[BasePermission]:
        """Get the permissions for the actions."""
        permission_classes = (AllowAny,) if self.action == "create" else (IsAuthenticated,)
        return [permission() for permission in permission_classes]
