"""This package contains all the serializers used by the friendships application."""
from my_game_list.friendships.serializers.friendship import FriendshipSerializer
from my_game_list.friendships.serializers.friendship_request import (
    FriendshipRequestCreateSerializer,
    FriendshipRequestSerializer,
)

__all__ = [
    "FriendshipSerializer",
    "FriendshipRequestCreateSerializer",
    "FriendshipRequestSerializer",
]
