"""Tests for platform model."""

import pytest

from my_game_list.games.models import Platform


@pytest.mark.django_db()
def test_platform_dunder_str() -> None:
    """Test the `Platform` dunder str method."""
    platform = Platform.objects.create(name="test_platform")
    assert str(platform) == platform.name
