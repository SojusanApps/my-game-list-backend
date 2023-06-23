"""Tests for game follow model."""
import pytest

from my_game_list.games.models import GameFollow


@pytest.mark.django_db()
def test_game_follow_dunder_str(game_follow_fixture: GameFollow) -> None:
    """Test the `GameFollow` dunder str method."""
    assert str(game_follow_fixture) == f"{game_follow_fixture.user.username} - {game_follow_fixture.game.title}"
