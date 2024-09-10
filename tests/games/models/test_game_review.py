"""Tests for game review model."""

import pytest

from my_game_list.games.models import GameReview


@pytest.mark.django_db()
def test_game_review_dunder_str(game_review_fixture: GameReview) -> None:
    """Test the `GameReview` dunder str method."""
    assert str(game_review_fixture) == f"{game_review_fixture.user.username} - {game_review_fixture.game.title}"
