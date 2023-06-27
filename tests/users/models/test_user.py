"""Tests for user app models."""
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from my_game_list.users.models import User as UserType

User: type["UserType"] = get_user_model()


@pytest.mark.django_db()
def test_user_dunder_str(user_fixture: "UserType") -> None:
    """Test the `User` dunder str method."""
    assert str(user_fixture) == f"{user_fixture.username} - {user_fixture.email}"
