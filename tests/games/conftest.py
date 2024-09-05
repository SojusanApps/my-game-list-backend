"""The fixtures used within games test module."""

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from my_game_list.games.models import (
    Developer,
    Game,
    GameFollow,
    GameList,
    GameListStatus,
    GameReview,
    Genre,
    Platform,
    Publisher,
)

if TYPE_CHECKING:
    from my_game_list.users.models import User as UserType

User: type["UserType"] = get_user_model()


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def developer_fixture() -> Developer:
    """A fixture with a test developer."""
    return Developer.objects.create(name="test_developer")


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def platform_fixture() -> Platform:
    """A fixture with a test platform."""
    return Platform.objects.create(name="test_platform")


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def publisher_fixture() -> Publisher:
    """A fixture with a test publisher."""
    return Publisher.objects.create(name="test_publisher")


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def genre_fixture() -> Genre:
    """A fixture with a test genre."""
    return Genre.objects.create(name="test_genre")


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def game_fixture(
    developer_fixture: Developer,
    platform_fixture: Platform,
    publisher_fixture: Publisher,
    genre_fixture: Genre,
) -> Game:
    """A fixture with a test game."""
    game = Game.objects.create(
        title="test_game",
        developer=developer_fixture,
        publisher=publisher_fixture,
    )
    game.genres.add(genre_fixture)
    game.platforms.add(platform_fixture)
    return game


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def game_review_fixture(user_fixture: "UserType", game_fixture: Game) -> GameReview:
    """A fixture with a test game review."""
    return GameReview.objects.create(
        review="test_review",
        game=game_fixture,
        user=user_fixture,
    )


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def game_list_fixture(user_fixture: "UserType", game_fixture: Game) -> GameList:
    """A fixture with a test game list."""
    return GameList.objects.create(
        score=5,
        status=GameListStatus.PLAN_TO_PLAY,
        game=game_fixture,
        user=user_fixture,
    )


@pytest.fixture()
@freeze_time("2023-06-22 16:47:12")
def game_follow_fixture(user_fixture: "UserType", game_fixture: Game) -> GameFollow:
    """A fixture with a test game follow."""
    return GameFollow.objects.create(game=game_fixture, user=user_fixture)
