import base64

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user(api_client: APIClient):
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@test.com",
        "avatar": base64.b64encode(b"Test").decode("utf-8"),
    }
    response = api_client.post(reverse("users:users-list"), data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"
