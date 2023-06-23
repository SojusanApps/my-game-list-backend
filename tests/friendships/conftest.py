"""This module contains the fixture for the friendships application."""
import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from my_game_list.friendships.models import Friendship, FriendshipRequest

User = get_user_model()


@pytest.fixture()
@freeze_time("2023-06-23 08:21:12")
def user_and_admin_friendship_request_fixture(user_fixture: User, admin_user_fixture: User) -> FriendshipRequest:
    """Add a friendship request between two users."""
    return FriendshipRequest.objects.create(sender=user_fixture, receiver=admin_user_fixture)


@pytest.fixture()
@freeze_time("2023-06-23 08:21:12")
def user_and_admin_friendship_fixture(user_fixture: User, admin_user_fixture: User) -> Friendship:
    """Add a relationship between user_fixture and admin_user_fixture."""
    return Friendship.objects.create(user=user_fixture, friend=admin_user_fixture)
