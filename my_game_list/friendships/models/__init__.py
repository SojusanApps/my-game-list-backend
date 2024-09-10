"""This package contains all models used by the friendships application."""

from my_game_list.friendships.models.friendship import Friendship
from my_game_list.friendships.models.friendship_request import FriendshipRequest

__all__ = [
    "Friendship",
    "FriendshipRequest",
]
