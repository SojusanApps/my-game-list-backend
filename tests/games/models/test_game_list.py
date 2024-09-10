"""Tests for game list model."""

import pytest

from my_game_list.games.models import GameList


@pytest.mark.django_db()
def test_game_list_dunder_str(game_list_fixture: GameList) -> None:
    """Test the `GameList` dunder str method."""
    assert str(game_list_fixture) == f"{game_list_fixture.user.username} - {game_list_fixture.game.title}"
