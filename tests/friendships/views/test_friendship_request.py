"""This module contains the tests for the friendship request views."""

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from my_game_list.friendships.models import Friendship, FriendshipRequest
from my_game_list.users.models import User as UserModel

User: type[UserModel] = get_user_model()


@freeze_time("2023-06-22 22:20:01")
@pytest.mark.django_db()
def test_create_model(
    user_fixture: UserModel,
    admin_user_fixture: UserModel,
    admin_authenticated_api_client: APIClient,
) -> None:
    """Check if creation of the new friendship request model is working properly."""
    initial_data = {
        "message": "Test message",
        "sender": user_fixture.pk,
        "receiver": admin_user_fixture.pk,
    }
    response = admin_authenticated_api_client.post(reverse("friendships:friendship-requests-list"), initial_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == initial_data


@pytest.mark.django_db()
def test_custom_action_accept(admin_authenticated_api_client: APIClient) -> None:
    """Check that after accepting a friendship request the friendship will be created."""
    sender_user = baker.make(User)
    receiver_user = baker.make(User)
    friendship_request = baker.make(FriendshipRequest, sender=sender_user, receiver=receiver_user)
    response = admin_authenticated_api_client.post(
        reverse("friendships:friendship-requests-accept", (friendship_request.pk,)),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "Success"}
    sender_friend: Friendship | None
    receiver_friend: Friendship | None
    if (sender_friend := sender_user.friends.first()) and (receiver_friend := receiver_user.friends.first()):
        assert sender_friend.friend == receiver_user
        assert receiver_friend.friend == sender_user
    else:
        raise Friendship.DoesNotExist
    assert FriendshipRequest.objects.count() == 0


@freeze_time("2023-06-23 18:21:41")
@pytest.mark.django_db()
def test_custom_action_reject(admin_authenticated_api_client: APIClient) -> None:
    """Check the friendship request reject."""
    sender_user = baker.make(User)
    receiver_user = baker.make(User)
    friendship_request = baker.make(FriendshipRequest, sender=sender_user, receiver=receiver_user)
    response = admin_authenticated_api_client.post(
        reverse("friendships:friendship-requests-reject", (friendship_request.pk,)),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Success"}
    friendship_request.refresh_from_db()
    assert str(friendship_request.rejected_at) == "2023-06-23 18:21:41+00:00"
