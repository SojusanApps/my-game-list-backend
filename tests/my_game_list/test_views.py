from django.test.client import Client
from django.urls import reverse
from rest_framework import status

from my_game_list import __version__


def test_version(client: Client):
    """Check if api version endpoint works properly."""
    response = client.get(reverse("api-version"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == ".".join(map(str, __version__))
