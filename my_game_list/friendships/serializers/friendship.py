from rest_framework import serializers

from my_game_list.friendships.models import Friendship
from my_game_list.users.serializers import UserSerializer


class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer for listing friendships."""

    user = UserSerializer()
    friend = UserSerializer()

    class Meta:
        model = Friendship
        fields = ("id", "created_at", "user", "friend")
        read_only_fields = ("id", "created_at")
