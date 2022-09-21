import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user_fixture():
    """
    Fixture creating and returning a user model instance
    with user name "test_user" and password "test".

    Returns:
        User: a created user instance
    """
    user = User.objects.create_user(username="test_user", password="test")
    return user


@pytest.fixture
def admin_fixture():
    """
    Fixture creating and returning a user model instance with superuser privileges,
    with user name "test_admin" and password "test".

    Returns:
        User: a created user instance
    """
    user = User.objects.create_superuser(username="test_admin", email=None, password="test")
    return user


@pytest.fixture
def api_client():
    return APIClient()
