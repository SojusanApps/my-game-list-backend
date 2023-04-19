from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Manager

User = get_user_model()


class FriendshipManager(Manager):
    """Manager for friendship."""

    def _get_friendship_model(self):
        return apps.get_model("friendships.Friendship")

    def _get_friendship_request_model(self):
        return apps.get_model("friendships.FriendshipRequest")

    def are_friends(self, first_user: User, second_user: User) -> bool:
        """Check if the given users are friends.

        Args:
            first_user (User): The first user in the relationship to check.
            second_user (User): The second user in the relationship to check.

        Returns:
            bool: True if users are friends, False otherwise.
        """
        friendship = self._get_friendship_model()
        return friendship.objects.filter(user=first_user, friend=second_user).exists()

    def request_is_sent(self, first_user: User, second_user: User) -> bool:
        """Check if the friendship request is sent to the user by a given user.

        Args:
            first_user (User): The first user in the relationship to check.
            second_user (User): The second user in the relationship to check.

        Returns:
            bool: True if the friendship request is sent to the user, False otherwise.
        """
        friendship_request = self._get_friendship_request_model()
        return friendship_request.objects.filter(sender=first_user, receiver=second_user).exists()
