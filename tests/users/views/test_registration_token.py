"""Tests for user registration with token issues."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

if TYPE_CHECKING:
    from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_register_user_with_invalid_token_should_succeed(api_client: APIClient) -> None:
    """
    Check if registration process is successful even if an invalid token is provided.

    Regression test for when an invalid token would cause a 401 despite permission being AllowAny.
    """
    data = {
        "username": "testuser_token",
        "password": "testpassword",
        "email": "test_token@test.com",
    }
    # Set an invalid token
    api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")

    response = api_client.post(reverse("users:users-list"), data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser_token"
