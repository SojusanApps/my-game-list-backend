"""This package contains all the filters used by the friendships application."""
from my_game_list.friendships.filters.friendship import FriendshipFilterSet
from my_game_list.friendships.filters.friendship_request import FriendshipRequestFilterSet

__all__ = [
    "FriendshipFilterSet",
    "FriendshipRequestFilterSet",
]
