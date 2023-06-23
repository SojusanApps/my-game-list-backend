"""This module contains serializers for the Friendship model."""
from rest_framework import serializers

from my_game_list.friendships.models import Friendship
from my_game_list.users.serializers import UserSerializer


class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer for listing friendships."""

    user = UserSerializer()
    friend = UserSerializer()

    class Meta:
        """Meta data for the friendship serializer."""

        model = Friendship
        fields = ("id", "created_at", "user", "friend")
        read_only_fields = ("id", "created_at")
