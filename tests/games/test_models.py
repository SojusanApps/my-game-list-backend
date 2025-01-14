"""Tests for games models."""

import pytest
from model_bakery import baker

from my_game_list.games.models import Company, Game, GameFollow, GameList, GameMedia, GameReview, Genre, Platform


@pytest.mark.django_db()
def test_company_dunder_str() -> None:
    """Test the `Company` dunder str method."""
    developer = baker.make(Company)
    assert str(developer) == developer.name


@pytest.mark.django_db()
def test_game_follow_dunder_str(game_follow_fixture: GameFollow) -> None:
    """Test the `GameFollow` dunder str method."""
    assert str(game_follow_fixture) == f"{game_follow_fixture.user.username} - {game_follow_fixture.game.title}"


@pytest.mark.django_db()
def test_game_list_dunder_str(game_list_fixture: GameList) -> None:
    """Test the `GameList` dunder str method."""
    assert str(game_list_fixture) == f"{game_list_fixture.user.username} - {game_list_fixture.game.title}"


@pytest.mark.django_db()
def test_game_review_dunder_str(game_review_fixture: GameReview) -> None:
    """Test the `GameReview` dunder str method."""
    assert str(game_review_fixture) == f"{game_review_fixture.user.username} - {game_review_fixture.game.title}"


@pytest.mark.django_db()
def test_game_dunder_str(game_fixture: Game) -> None:
    """Test the `Game` dunder str method."""
    assert str(game_fixture) == game_fixture.title


@pytest.mark.django_db()
def test_genre_dunder_str() -> None:
    """Test the `Genre` dunder str method."""
    genre = baker.make(Genre)
    assert str(genre) == genre.name


@pytest.mark.django_db()
def test_platform_dunder_str() -> None:
    """Test the `Platform` dunder str method."""
    platform = baker.make(Platform)
    assert str(platform) == platform.name


@pytest.mark.django_db()
def test_game_media_dunder_str() -> None:
    """Test the `GameMedia` dunder str method."""
    game_media = baker.make(GameMedia)
    assert str(game_media) == game_media.name
