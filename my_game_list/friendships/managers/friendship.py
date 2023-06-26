"""This module contains the managers for the Friendship model."""
from typing import TYPE_CHECKING

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Manager

if TYPE_CHECKING:
    from my_game_list.friendships.models import Friendship, FriendshipRequest

User = get_user_model()


class FriendshipManager(Manager):
    """Manager for friendship."""

    @staticmethod
    def _get_friendship_model() -> "Friendship":
        return apps.get_model("friendships.Friendship")

    @staticmethod
    def _get_friendship_request_model() -> "FriendshipRequest":
        return apps.get_model("friendships.FriendshipRequest")

    def are_friends(self: "FriendshipManager", first_user: User, second_user: User) -> bool:
        """Check if the given users are friends.

        Args:
            first_user (User): The first user in the relationship to check.
            second_user (User): The second user in the relationship to check.

        Returns:
            bool: True if users are friends, False otherwise.
        """
        friendship = self._get_friendship_model()
        return friendship.objects.filter(user=first_user, friend=second_user).exists()

    def request_is_sent(self: "FriendshipManager", first_user: User, second_user: User) -> bool:
        """Check if the friendship request is sent to the user by a given user.

        Args:
            first_user (User): The first user in the relationship to check.
            second_user (User): The second user in the relationship to check.

        Returns:
            bool: True if the friendship request is sent to the user, False otherwise.
        """
        friendship_request = self._get_friendship_request_model()
        return friendship_request.objects.filter(sender=first_user, receiver=second_user).exists()
