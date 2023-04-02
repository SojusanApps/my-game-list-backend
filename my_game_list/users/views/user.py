from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from my_game_list.users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """ViewSet is responsible for creating, listing, and retrieving user information."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserCreateSerializer if self.action == "create" else UserSerializer

    def get_permissions(self):
        permission_classes = (AllowAny,) if self.action == "create" else (IsAuthenticated,)
        return [permission() for permission in permission_classes]
