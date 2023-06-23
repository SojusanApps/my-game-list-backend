"""Tests for publisher model."""
import pytest

from my_game_list.games.models import Publisher


@pytest.mark.django_db()
def test_publisher_dunder_str() -> None:
    """Test the `Publisher` dunder str method."""
    publisher = Publisher.objects.create(name="test_publisher")
    assert str(publisher) == publisher.name
