"""Tests for genre model."""

import pytest
from model_bakery import baker

from my_game_list.games.models import Genre


@pytest.mark.django_db()
def test_genre_dunder_str() -> None:
    """Test the `Genre` dunder str method."""
    genre = baker.make(Genre)
    assert str(genre) == genre.name
