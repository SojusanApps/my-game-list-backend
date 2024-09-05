"""This module contains the viewsets for the Friendship model."""

from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from my_game_list.friendships.filters import FriendshipFilterSet
from my_game_list.friendships.models import Friendship
from my_game_list.friendships.serializers import FriendshipSerializer

User = get_user_model()


class FriendshipViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet["Friendship"]):
    """All views related to friendship."""

    queryset = Friendship.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FriendshipSerializer
    filterset_class = FriendshipFilterSet
