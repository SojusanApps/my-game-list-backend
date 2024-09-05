"""Tests for developer model."""

import pytest

from my_game_list.games.models import Developer


@pytest.mark.django_db()
def test_developer_dunder_str() -> None:
    """Test the `Developer` dunder str method."""
    developer = Developer.objects.create(name="test_developer")
    assert str(developer) == developer.name
