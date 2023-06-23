"""Tests for user app models."""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db()
def test_user_dunder_str(user_fixture: User) -> None:
    """Test the `User` dunder str method."""
    assert str(user_fixture) == f"{user_fixture.username} - {user_fixture.email}"
