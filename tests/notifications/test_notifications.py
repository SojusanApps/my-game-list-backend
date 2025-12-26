"""Test notifications functionality."""

import pytest
from django.contrib.auth import get_user_model

from my_game_list.notifications.models import Notification
from my_game_list.notifications.utils import notify_send

User = get_user_model()


@pytest.mark.django_db()
def test_notify_send() -> None:
    """Test sending a notification."""
    user1 = User.objects.create_user(username="user1", password="password", email="user1@email.com")  # noqa: S106
    user2 = User.objects.create_user(username="user2", password="password", email="user2@email.com")  # noqa: S106

    notification = notify_send(sender=user1, recipient=user2, verb="sent you a friend request")

    assert Notification.objects.count() == 1
    assert notification.recipient == user2
    assert notification.actor == user1
    assert notification.verb == "sent you a friend request"
    assert notification.unread is True


@pytest.mark.django_db()
def test_mark_as_read() -> None:
    """Test marking a notification as read."""
    user1 = User.objects.create_user(username="user1", password="password", email="user1@email.com")  # noqa: S106
    user2 = User.objects.create_user(username="user2", password="password", email="user2@email.com")  # noqa: S106

    notification = notify_send(sender=user1, recipient=user2, verb="verb")
    assert notification.unread is True

    notification.mark_as_read()
    assert notification.unread is False
