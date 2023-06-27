"""This package contains all the admin models used by the friendships application."""
from my_game_list.friendships.admin.friendship import FriendshipAdmin
from my_game_list.friendships.admin.friendship_request import FriendshipRequestAdmin

__all__ = [
    "FriendshipAdmin",
    "FriendshipRequestAdmin",
]
