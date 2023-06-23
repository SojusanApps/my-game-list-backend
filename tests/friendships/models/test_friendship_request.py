"""Tests for friendship request model."""
import pytest
from django.contrib.auth import get_user_model

from my_game_list.friendships.models import FriendshipRequest
from my_game_list.my_game_list.exceptions import ConflictException

User = get_user_model()


@pytest.mark.django_db()
def test_friendship_request_dunder_str(user_fixture: User, admin_user_fixture: User) -> None:
    """Test the `FriendshipRequest` dunder str method."""
    friendship_request = FriendshipRequest.objects.create(sender=user_fixture, receiver=admin_user_fixture)
    assert str(friendship_request) == (
        f"From: {friendship_request.sender.username} To: {friendship_request.receiver.username}"
    )


@pytest.mark.django_db()
def test_double_rejection_error(user_fixture: User, admin_user_fixture: User) -> None:
    """Check for double rejection error."""
    friendship_request = FriendshipRequest.objects.create(sender=user_fixture, receiver=admin_user_fixture)
    friendship_request.reject()

    with pytest.raises(ConflictException) as exception_info:
        friendship_request.reject()

    assert str(exception_info.value.detail) == "This friendship request is already rejected."
