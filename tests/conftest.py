"""Includes global scope fixtures. They can be used in all tests."""

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from my_game_list.users.models import User as UserModel

User: type[UserModel] = get_user_model()


@pytest.fixture
@freeze_time("2023-05-25 12:01:12")
def user_fixture() -> UserModel:
    """Create a new user.

    Fixture creating and returning a user model instance with user name "test_user" and password "test".

    Returns:
        User: a created user instance
    """
    return baker.make(User, username="test_user", email="test@email.com", password="test")  # noqa: S106


@pytest.fixture
@freeze_time("2023-05-25 14:21:13")
def admin_user_fixture() -> UserModel:
    """Create a new admin.

    Fixture creating and returning a user model instance with superuser privileges,
    with user name "test_admin" and password "test".

    Returns:
        User: a created user instance
    """
    return baker.make(
        User,
        username="test_admin",
        email="test_admin@email.com",
        password="test",  # noqa: S106
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def api_client() -> APIClient:
    """Fixture providing the API client."""
    return APIClient()


@pytest.fixture
def authenticated_api_client(user_fixture: UserModel, api_client: APIClient) -> APIClient:
    """Fixture providing the API client that is authorized as a simple user."""
    api_client.force_authenticate(user_fixture)

    return api_client


@pytest.fixture
def admin_authenticated_api_client(admin_user_fixture: UserModel, api_client: APIClient) -> APIClient:
    """Fixture providing the API client that is authorized as a admin user."""
    api_client.force_authenticate(admin_user_fixture)

    return api_client
