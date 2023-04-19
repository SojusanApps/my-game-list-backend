import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def user_fixture():
    """Create a new user.

    Fixture creating and returning a user model instance with user name "test_user" and password "test".

    Returns:
        User: a created user instance
    """
    return User.objects.create_user(username="test_user", password="test")  # noqa: S106


@pytest.fixture()
def admin_fixture():
    """Create a new admin.

    Fixture creating and returning a user model instance with superuser privileges,
    with user name "test_admin" and password "test".

    Returns:
        User: a created user instance
    """
    return User.objects.create_superuser(username="test_admin", email=None, password="test")  # noqa: S106


@pytest.fixture()
def api_client():
    """Fixture providing the API client."""
    return APIClient()
