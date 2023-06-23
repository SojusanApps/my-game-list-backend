"""Tests for game model."""
import pytest

from my_game_list.games.models import Game


@pytest.mark.django_db()
def test_game_dunder_str(game_fixture: Game) -> None:
    """Test the `Game` dunder str method."""
    assert str(game_fixture) == game_fixture.title
