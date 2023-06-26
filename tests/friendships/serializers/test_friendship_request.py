"""This module contains tests for the friendship request serializers."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError

from my_game_list.friendships.models import Friendship, FriendshipRequest
from my_game_list.friendships.serializers import FriendshipRequestCreateSerializer

User = get_user_model()


@pytest.mark.django_db()
def test_friendship_to_myself(user_fixture: User) -> None:
    """Check for creation a friendship to the same user."""
    serializer = FriendshipRequestCreateSerializer(data={"sender": user_fixture.pk, "receiver": user_fixture.pk})

    with pytest.raises(ValidationError) as exception_info:
        serializer.is_valid(raise_exception=True)

    assert str(exception_info.value.detail["non_field_errors"][0]) == "Can't create friendship request to yourself."


@pytest.mark.django_db()
def test_users_are_already_friends(
    user_fixture: User,
    admin_user_fixture: User,
    user_and_admin_friendship_fixture: Friendship,  # noqa: ARG001
) -> None:
    """Test that users cant create a duplicated relationship."""
    serializer = FriendshipRequestCreateSerializer(data={"sender": user_fixture.pk, "receiver": admin_user_fixture.pk})

    with pytest.raises(ValidationError) as exception_info:
        serializer.is_valid(raise_exception=True)

    assert str(exception_info.value.detail["non_field_errors"][0]) == "You are already friends."


@pytest.mark.django_db()
def test_you_already_sent_friendship_request(
    user_fixture: User,
    admin_user_fixture: User,
    user_and_admin_friendship_request_fixture: FriendshipRequest,  # noqa: ARG001
) -> None:
    """Test that user can't send a another friendship request to the same user."""
    serializer = FriendshipRequestCreateSerializer(data={"sender": user_fixture.pk, "receiver": admin_user_fixture.pk})

    with pytest.raises(ValidationError) as exception_info:
        serializer.is_valid(raise_exception=True)

    assert str(exception_info.value.detail["non_field_errors"][0]) == (
        "You already sent a friendship request to this user."
    )


@pytest.mark.django_db()
def test_user_already_sent_friendship_request(
    user_fixture: User,
    admin_user_fixture: User,
    user_and_admin_friendship_request_fixture: FriendshipRequest,  # noqa: ARG001
) -> None:
    """Test that user can't send a another friendship request to the same user."""
    serializer = FriendshipRequestCreateSerializer(data={"sender": admin_user_fixture.pk, "receiver": user_fixture.pk})

    with pytest.raises(ValidationError) as exception_info:
        serializer.is_valid(raise_exception=True)

    assert str(exception_info.value.detail["non_field_errors"][0]) == (
        "This user already sent a friendship request to you."
    )
