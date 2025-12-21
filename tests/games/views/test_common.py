"""This module contains tests for the common functionality for the viewsets in the game application."""

from collections.abc import Mapping
from typing import Any
from unittest.mock import ANY

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from my_game_list.games.models import (
    Company,
    Game,
    GameListStatus,
    Genre,
    Platform,
)
from my_game_list.users.models import User as UserModel

User: type[UserModel] = get_user_model()
FORBIDDEN_DETAIL = "You do not have permission to perform this action."
GAME_USER_DEPENDENT_LIST_VIEWNAMES = [
    "games:game-reviews-list",
    "games:game-lists-list",
    "games:game-follows-list",
]
GAME_USER_DEPENDENT_DETAIL_VIEWNAMES = [
    "games:game-reviews-detail",
    "games:game-lists-detail",
    "games:game-follows-detail",
]


@pytest.mark.parametrize(
    "viewname",
    [
        pytest.param(
            "games:companies-list",
            id="Check forbidden access for the creation of company.",
        ),
        pytest.param(
            "games:games-list",
            id="Check forbidden access for the creation of game.",
        ),
        pytest.param(
            "games:genres-list",
            id="Check forbidden access for the creation of genre.",
        ),
        pytest.param(
            "games:platforms-list",
            id="Check forbidden access for the creation of platform.",
        ),
        pytest.param(
            "games:game-medias-list",
            id="Check forbidden access for the creation of game media.",
        ),
    ],
)
@pytest.mark.django_db()
def test_forbidden_access_list(viewname: str, authenticated_api_client: APIClient) -> None:
    """Check if the unauthorized user did not have access to the protected endpoints."""
    response = authenticated_api_client.post(reverse(viewname))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": FORBIDDEN_DETAIL}


@pytest.mark.parametrize(
    "viewname",
    [
        pytest.param(
            "games:game-follows-list",
            id="Check unauthorized access for the creation of game follow.",
        ),
        pytest.param(
            "games:game-lists-list",
            id="Check unauthorized access for the creation of game list.",
        ),
        pytest.param(
            "games:game-reviews-list",
            id="Check unauthorized access for the creation of game review.",
        ),
    ],
)
@pytest.mark.django_db()
def test_unauthorized_access_list(viewname: str, api_client: APIClient) -> None:
    """Check if the unauthorized user did not have access to the protected endpoints."""
    response = api_client.post(reverse(viewname))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Authentication credentials were not provided."}


@pytest.mark.parametrize(
    "method",
    [
        pytest.param("put", id="PUT method"),
        pytest.param("patch", id="PATCH method"),
        pytest.param("delete", id="DELETE method"),
    ],
)
@pytest.mark.parametrize(
    "viewname",
    [
        pytest.param(
            "games:companies-detail",
            id="Check forbidden access for the company with given id.",
        ),
        pytest.param(
            "games:games-detail",
            id="Check forbidden access for the game with given id.",
        ),
        pytest.param(
            "games:genres-detail",
            id="Check forbidden access for the genre with given id.",
        ),
        pytest.param(
            "games:platforms-detail",
            id="Check forbidden access for the platform with given id.",
        ),
        pytest.param(
            "games:game-medias-detail",
            id="Check forbidden access for the game media with given id.",
        ),
    ],
)
@pytest.mark.django_db()
def test_forbidden_access_detail(method: str, viewname: str, authenticated_api_client: APIClient) -> None:
    """Check if the unauthorized user did not have access to the protected endpoints."""
    response = getattr(authenticated_api_client, method)(reverse(viewname, (1,)))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": FORBIDDEN_DETAIL}


@pytest.mark.parametrize(
    "viewname",
    [
        pytest.param(
            "games:game-follows-detail",
            id="Check unauthorized access for the given game follow.",
        ),
        pytest.param(
            "games:game-lists-detail",
            id="Check unauthorized access for the given game list.",
        ),
        pytest.param(
            "games:game-reviews-detail",
            id="Check unauthorized access for the given game review.",
        ),
    ],
)
@pytest.mark.django_db()
def test_unauthorized_access_detail(viewname: str, api_client: APIClient) -> None:
    """Check if the unauthorized user did not have access to the protected endpoints."""
    response = api_client.post(reverse(viewname, (1,)))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Authentication credentials were not provided."}


@pytest.mark.parametrize(
    ("viewname", "fixture_name", "expected_result"),
    [
        pytest.param(
            "games:companies-list",
            "developer_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "name": ANY,
                        "company_logo_id": "",
                        "igdb_id": ANY,
                        "igdb_updated_at": ANY,
                    },
                ],
            },
            id="Test list endpoint for company.",
        ),
        pytest.param(
            "games:game-follows-list",
            "game_follow_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "game": ANY,
                        "user": ANY,
                        "created_at": "2023-06-22T16:47:12Z",
                    },
                ],
            },
            id="Test list endpoint for game follow.",
        ),
        pytest.param(
            "games:game-lists-list",
            "game_list_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "title": ANY,
                        "game_id": ANY,
                        "game_cover_image": ANY,
                        "user": ANY,
                        "score": 5,
                        "status": GameListStatus.PLAN_TO_PLAY.label,
                        "status_code": GameListStatus.PLAN_TO_PLAY.value,
                        "last_modified_at": "2023-06-22T16:47:12Z",
                        "created_at": "2023-06-22T16:47:12Z",
                        "owned_on": ANY,
                    },
                ],
            },
            id="Test list endpoint for game list.",
        ),
        pytest.param(
            "games:game-reviews-list",
            "game_review_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "game": ANY,
                        "user": ANY,
                        "score": None,
                        "review": "test_review",
                        "created_at": "2023-06-22T16:47:12Z",
                    },
                ],
            },
            id="Test list endpoint for game review.",
        ),
        pytest.param(
            "games:games-list",
            "game_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "igdb_id": ANY,
                        "igdb_updated_at": ANY,
                        "cover_image_id": ANY,
                        "created_at": "2023-06-22T16:47:12Z",
                        "summary": "",
                        "developer": {
                            "id": ANY,
                            "name": ANY,
                            "company_logo_id": "",
                            "igdb_id": ANY,
                            "igdb_updated_at": ANY,
                        },
                        "genres": [{"id": ANY, "name": ANY, "igdb_id": ANY, "igdb_updated_at": ANY}],
                        "id": ANY,
                        "last_modified_at": "2023-06-22T16:47:12Z",
                        "platforms": [
                            {"id": ANY, "name": ANY, "igdb_id": ANY, "abbreviation": "", "igdb_updated_at": ANY},
                        ],
                        "publisher": {
                            "id": ANY,
                            "name": ANY,
                            "company_logo_id": ANY,
                            "igdb_id": ANY,
                            "igdb_updated_at": ANY,
                        },
                        "release_date": None,
                        "title": ANY,
                        "average_score": 0.0,
                        "members_count": 0,
                        "popularity": 1,
                        "rank_position": 1,
                        "scores_count": 0,
                    },
                ],
            },
            id="Test list endpoint for game.",
        ),
        pytest.param(
            "games:genres-list",
            "genre_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "name": ANY,
                        "igdb_id": ANY,
                        "igdb_updated_at": ANY,
                    },
                ],
            },
            id="Test list endpoint for genre.",
        ),
        pytest.param(
            "games:platforms-list",
            "platform_fixture",
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "name": ANY,
                        "igdb_id": ANY,
                        "igdb_updated_at": ANY,
                        "abbreviation": "",
                    },
                ],
            },
            id="Test list endpoint for platform.",
        ),
        pytest.param(
            "games:game-medias-list",
            "game_media_fixture",
            {
                "count": 6,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                    {
                        "id": ANY,
                        "name": ANY,
                    },
                ],
            },
            id="Test list endpoint for game media.",
        ),
    ],
)
@pytest.mark.django_db()
def test_list_model(
    request: pytest.FixtureRequest,
    viewname: str,
    fixture_name: str,
    expected_result: Mapping[str, Any],
    authenticated_api_client: APIClient,
) -> None:
    """Get the list of objects for the given model."""
    request.getfixturevalue(fixture_name)
    response = authenticated_api_client.get(reverse(viewname))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result


@pytest.mark.parametrize(
    ("viewname", "fixture_name", "expected_result"),
    [
        pytest.param(
            "games:companies-detail",
            "developer_fixture",
            {
                "id": ANY,
                "name": ANY,
                "company_logo_id": "",
                "igdb_id": ANY,
                "igdb_updated_at": ANY,
            },
            id="Get the company by id.",
        ),
        pytest.param(
            "games:game-follows-detail",
            "game_follow_fixture",
            {
                "id": ANY,
                "game": ANY,
                "user": ANY,
                "created_at": "2023-06-22T16:47:12Z",
            },
            id="Get the game follow by id.",
        ),
        pytest.param(
            "games:game-lists-detail",
            "game_list_fixture",
            {
                "id": ANY,
                "title": ANY,
                "game_id": ANY,
                "game_cover_image": ANY,
                "user": ANY,
                "score": 5,
                "status": GameListStatus.PLAN_TO_PLAY.label,
                "status_code": GameListStatus.PLAN_TO_PLAY.value,
                "last_modified_at": "2023-06-22T16:47:12Z",
                "created_at": "2023-06-22T16:47:12Z",
                "owned_on": ANY,
            },
            id="Get the game list by id.",
        ),
        pytest.param(
            "games:game-reviews-detail",
            "game_review_fixture",
            {
                "id": ANY,
                "game": ANY,
                "user": ANY,
                "review": "test_review",
                "score": None,
                "created_at": "2023-06-22T16:47:12Z",
            },
            id="Get the game review by id.",
        ),
        pytest.param(
            "games:games-detail",
            "game_fixture",
            {
                "cover_image_id": ANY,
                "created_at": "2023-06-22T16:47:12Z",
                "summary": "",
                "igdb_id": ANY,
                "igdb_updated_at": ANY,
                "developer": {
                    "id": ANY,
                    "name": ANY,
                    "company_logo_id": "",
                    "igdb_id": ANY,
                    "igdb_updated_at": ANY,
                },
                "genres": [{"id": ANY, "name": ANY, "igdb_id": ANY, "igdb_updated_at": ANY}],
                "id": ANY,
                "last_modified_at": "2023-06-22T16:47:12Z",
                "platforms": [{"id": ANY, "name": ANY, "igdb_id": ANY, "abbreviation": "", "igdb_updated_at": ANY}],
                "publisher": {
                    "id": ANY,
                    "name": ANY,
                    "company_logo_id": "",
                    "igdb_id": ANY,
                    "igdb_updated_at": ANY,
                },
                "release_date": None,
                "title": ANY,
                "average_score": 0.0,
                "members_count": 0,
                "popularity": 1,
                "rank_position": 1,
                "scores_count": 0,
            },
            id="Get the game by id.",
        ),
        pytest.param(
            "games:genres-detail",
            "genre_fixture",
            {
                "id": ANY,
                "name": ANY,
                "igdb_id": ANY,
                "igdb_updated_at": ANY,
            },
            id="Get the genre by id.",
        ),
        pytest.param(
            "games:platforms-detail",
            "platform_fixture",
            {
                "id": ANY,
                "name": ANY,
                "igdb_id": ANY,
                "igdb_updated_at": ANY,
                "abbreviation": "",
            },
            id="Get the platform by id.",
        ),
        pytest.param(
            "games:game-medias-detail",
            "game_media_fixture",
            {
                "id": ANY,
                "name": ANY,
            },
            id="Get the game media by id.",
        ),
    ],
)
@pytest.mark.django_db()
def test_get_model_detail(
    request: pytest.FixtureRequest,
    viewname: str,
    fixture_name: str,
    expected_result: Mapping[str, Any],
    authenticated_api_client: APIClient,
) -> None:
    """Check that the user can get the model instance data with the given id."""
    model_instance = request.getfixturevalue(fixture_name)
    response = authenticated_api_client.get(reverse(viewname, (model_instance.pk,)))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result


@freeze_time("2023-06-22 22:20:01")
@pytest.mark.parametrize(
    ("viewname", "initial_data", "expected_result"),
    [
        pytest.param(
            "games:companies-list",
            {
                "name": "created_developer",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "id": ANY,
                "company_logo_id": "",
            },
            id="Creation of the company.",
        ),
        pytest.param(
            "games:game-follows-list",
            {},
            {
                "id": ANY,
                "created_at": "2023-06-22T22:20:01Z",
            },
            id="Create a new game follow.",
        ),
        pytest.param(
            "games:game-lists-list",
            {
                "status": GameListStatus.PLAN_TO_PLAY.value,
                "score": 1,
            },
            {
                "id": ANY,
                "score": 1,
                "status": GameListStatus.PLAN_TO_PLAY.value,
                "created_at": "2023-06-22T22:20:01Z",
                "last_modified_at": "2023-06-22T22:20:01Z",
                "owned_on": ANY,
            },
            id="Create a new game list.",
        ),
        pytest.param(
            "games:game-reviews-list",
            {
                "review": "test review - new",
            },
            {
                "id": ANY,
                "created_at": "2023-06-22T22:20:01Z",
            },
            id="Create a new game review.",
        ),
        pytest.param(
            "games:games-list",
            {
                "title": "New created game",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "id": ANY,
                "cover_image_id": ANY,
                "created_at": "2023-06-22T22:20:01Z",
                "last_modified_at": "2023-06-22T22:20:01Z",
                "release_date": None,
                "summary": "",
            },
            id="Create a new game.",
        ),
        pytest.param(
            "games:genres-list",
            {
                "name": "created_genre",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "id": ANY,
            },
            id="Creation of the genre.",
        ),
        pytest.param(
            "games:platforms-list",
            {
                "abbreviation": "TP",
                "name": "created_platform",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "id": ANY,
            },
            id="Creation of the platform.",
        ),
        pytest.param(
            "games:game-medias-list",
            {
                "name": "created_media",
            },
            {
                "id": ANY,
            },
            id="Creation of the game media.",
        ),
    ],
)
@pytest.mark.django_db()
def test_create_model(
    viewname: str,
    initial_data: dict[str, Any],
    expected_result: dict[str, Any],
    admin_user_fixture: UserModel,
    developer_fixture: Company,
    publisher_fixture: Company,
    genre_fixture: Genre,
    platform_fixture: Platform,
    game_fixture: Game,
    admin_authenticated_api_client: APIClient,
) -> None:
    """Check if creation of the new dictionary model is working properly."""
    if viewname == "games:games-list":
        initial_data |= {
            "developer": developer_fixture.pk,
            "publisher": publisher_fixture.pk,
            "genres": [genre_fixture.pk],
            "platforms": [platform_fixture.pk],
        }
    elif viewname in GAME_USER_DEPENDENT_LIST_VIEWNAMES:
        initial_data |= {"user": admin_user_fixture.pk, "game": game_fixture.pk}
    response = admin_authenticated_api_client.post(reverse(viewname), initial_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == initial_data | expected_result


@freeze_time("2023-06-22 22:20:01")
@pytest.mark.parametrize(
    "method",
    [
        pytest.param(
            "put",
            id="PUT update test.",
        ),
        pytest.param(
            "patch",
            id="PATCH update test.",
        ),
    ],
)
@pytest.mark.parametrize(
    ("viewname", "fixture_name", "update_data", "expected_result"),
    [
        pytest.param(
            "games:companies-detail",
            "developer_fixture",
            {
                "name": "created_developer",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "company_logo_id": "",
            },
            id="Update of the company.",
        ),
        pytest.param(
            "games:game-follows-detail",
            "game_follow_fixture",
            {},
            {
                "created_at": "2023-06-22T16:47:12Z",
            },
            id="Update a game follow.",
        ),
        pytest.param(
            "games:game-lists-detail",
            "game_list_fixture",
            {
                "score": 10,
                "status": GameListStatus.COMPLETED.value,
            },
            {
                "score": 10,
                "status": GameListStatus.COMPLETED.value,
                "created_at": "2023-06-22T16:47:12Z",
                "last_modified_at": "2023-06-22T22:20:01Z",
                "owned_on": ANY,
            },
            id="Update a game list.",
        ),
        pytest.param(
            "games:game-reviews-detail",
            "game_review_fixture",
            {
                "review": "Updated review.",
            },
            {
                "created_at": "2023-06-22T16:47:12Z",
            },
            id="Update a game review.",
        ),
        pytest.param(
            "games:games-detail",
            "game_fixture",
            {
                "title": "Updated title",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {
                "created_at": "2023-06-22T16:47:12Z",
                "last_modified_at": "2023-06-22T22:20:01Z",
                "release_date": None,
                "summary": "",
                "cover_image_id": ANY,
            },
            id="Update a game.",
        ),
        pytest.param(
            "games:genres-detail",
            "genre_fixture",
            {
                "name": "updated_genre",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {},
            id="Update of the genre.",
        ),
        pytest.param(
            "games:platforms-detail",
            "platform_fixture",
            {
                "abbreviation": "",
                "name": "updated_platform",
                "igdb_id": 123,
                "igdb_updated_at": "2023-06-22T22:20:01Z",
            },
            {},
            id="Update of the platform.",
        ),
        pytest.param(
            "games:game-medias-detail",
            "game_media_fixture",
            {
                "name": "updated_media",
            },
            {},
            id="Update of the game media.",
        ),
    ],
)
@pytest.mark.django_db()
def test_update_model(
    request: pytest.FixtureRequest,
    method: str,
    viewname: str,
    fixture_name: str,
    update_data: dict[str, Any],
    expected_result: dict[str, Any],
    admin_authenticated_api_client: APIClient,
) -> None:
    """Check if updates method works properly for game models."""
    if viewname == "games:games-detail":
        update_data |= {
            "developer": baker.make(Company).pk,
            "publisher": baker.make(Company).pk,
            "genres": [baker.make(Genre).pk],
            "platforms": [baker.make(Platform).pk],
        }
    elif viewname in GAME_USER_DEPENDENT_DETAIL_VIEWNAMES:
        update_data |= {
            "user": baker.make(User).pk,
            "game": baker.make(Game).pk,
        }
    model_instance = request.getfixturevalue(fixture_name)
    response = getattr(admin_authenticated_api_client, method)(
        reverse(viewname, (model_instance.pk,)),
        update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == update_data | expected_result | {"id": model_instance.pk}


@pytest.mark.parametrize(
    ("viewname", "fixture_name", "total_count_after_deletion"),
    [
        pytest.param(
            "games:companies-detail",
            "developer_fixture",
            0,
            id="Delete the company.",
        ),
        pytest.param(
            "games:game-follows-detail",
            "game_follow_fixture",
            0,
            id="Delete the game follow.",
        ),
        pytest.param(
            "games:game-lists-detail",
            "game_list_fixture",
            0,
            id="Delete the game list.",
        ),
        pytest.param(
            "games:game-reviews-detail",
            "game_review_fixture",
            0,
            id="Delete the game review.",
        ),
        pytest.param(
            "games:games-detail",
            "game_fixture",
            0,
            id="Delete the game.",
        ),
        pytest.param(
            "games:genres-detail",
            "genre_fixture",
            0,
            id="Delete the genre.",
        ),
        pytest.param(
            "games:platforms-detail",
            "platform_fixture",
            0,
            id="Delete the platform.",
        ),
        pytest.param(
            "games:game-medias-detail",
            "game_media_fixture",
            5,
            id="Delete the game media.",
        ),
    ],
)
@pytest.mark.django_db()
def test_delete_model(
    request: pytest.FixtureRequest,
    viewname: str,
    fixture_name: str,
    total_count_after_deletion: int,
    admin_authenticated_api_client: APIClient,
) -> None:
    """Check if deletion of the game model works properly."""
    model_instance = request.getfixturevalue(fixture_name)
    response = admin_authenticated_api_client.delete(reverse(viewname, (model_instance.pk,)))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert model_instance.__class__.objects.count() == total_count_after_deletion
