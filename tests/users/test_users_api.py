import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user(api_client: APIClient):
    data = {
        "username": "testuser",
        "password": "testpassword",
        "gender": "M",
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "Doe",
        "avatar": open("tests/resources/test_image.png", "rb"),
    }
    response = api_client.post(reverse("users:users-list"), data)

    print(f"\033[92m {response.json()} \033[0m")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"
