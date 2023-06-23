"""Tests for genre model."""
import pytest

from my_game_list.games.models import Genre


@pytest.mark.django_db()
def test_genre_dunder_str() -> None:
    """Test the `Genre` dunder str method."""
    genre = Genre.objects.create(name="test_genre")
    assert str(genre) == genre.name
