"""Module with the logic regarding the IGDB interaction."""

import time
from typing import Any, NotRequired, Self, TypedDict, cast

import requests
from django.conf import settings
from requests_futures.sessions import FuturesSession
from rest_framework import status


class IGDBEndpoints:
    """IGDB endpoints used in the application."""

    GENRES = "genres"
    PLATFORMS = "platforms"
    GAMES = "games"
    COMPANIES = "companies"


class IGDBAuthenticationResponse(TypedDict):
    """TypedDict representing the data structure for IGDB authentication success response."""

    access_token: str
    expires_in: int
    token_type: str


class IGDBImageResponse(TypedDict):
    """TypedDict representing the data structure for IGDB image response."""

    id: int
    image_id: str


class IGDBPlatformResponse(TypedDict):
    """TypedDict representing the data structure for IGDB platform response."""

    id: int
    name: str
    abbreviation: NotRequired[str]


class IGDBGenreResponse(TypedDict):
    """TypedDict representing the data structure for IGDB genre response."""

    id: int
    name: str


class IGDBCompanyResponse(TypedDict):
    """TypedDict representing the data structure for IGDB company response."""

    id: int
    name: str
    logo: NotRequired[IGDBImageResponse]


class IGDBInvolvedCompanyResponse(TypedDict):
    """TypedDict representing the data structure for IGDB involved company response."""

    id: int
    company: int
    developer: bool
    publisher: bool


class IGDBGameResponse(TypedDict):
    """TypeDict representing the data structure for IGDB game response."""

    id: int
    cover: NotRequired[IGDBImageResponse]
    first_release_date: NotRequired[int]
    genres: NotRequired[list[int]]
    involved_companies: NotRequired[list[IGDBInvolvedCompanyResponse]]
    name: str
    platforms: NotRequired[list[int]]
    summary: NotRequired[str]


class IGDBInteractionError(Exception):
    """IGDB interaction error."""


class IGDBWrapper:
    """IGDB wrapper class."""

    IGDB_AUTHENTICATION_URL = (
        "https://id.twitch.tv/oauth2/token"
        f"?client_id={settings.IGDB_CLIENT_ID}&client_secret={settings.IGDB_CLIENT_SECRET}&grant_type=client_credentials"
    )
    IGDB_BASE_URL = "https://api.igdb.com/v4/"
    QUERY_ITEM_LIMIT = 500

    def __init__(self: Self) -> None:
        """Initialize the IGDB wrapper."""
        access_token = self.get_igdb_access_token()
        self.basic_auth_headers = {
            "Client-ID": settings.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {access_token}",
        }

    def get_igdb_access_token(self: Self) -> str:
        """Get the IGDB access token."""
        response = requests.post(self.IGDB_AUTHENTICATION_URL, timeout=10)
        if response.status_code != status.HTTP_200_OK:
            error_message = f"Unable to get the access_token for IGDB. Response: {response.json()}"
            raise IGDBInteractionError(error_message)
        return cast(IGDBAuthenticationResponse, response.json())["access_token"]

    def _cast_response(
        self: Self,
        endpoint: str,
        response_json: dict[str, Any],
    ) -> list[IGDBPlatformResponse] | list[IGDBGenreResponse] | list[IGDBCompanyResponse] | list[IGDBGameResponse]:
        """Cast the response to the correct type for the endpoint."""
        match endpoint:
            case IGDBEndpoints.PLATFORMS:
                return cast(list[IGDBPlatformResponse], response_json)
            case IGDBEndpoints.GENRES:
                return cast(list[IGDBGenreResponse], response_json)
            case IGDBEndpoints.COMPANIES:
                return cast(list[IGDBCompanyResponse], response_json)
            case IGDBEndpoints.GAMES:
                return cast(list[IGDBGameResponse], response_json)
            case _:
                error_message = f"Unknown endpoint: {endpoint}."
                raise IGDBInteractionError(error_message)

    def api_request(
        self: Self,
        endpoint: str,
        query: str,
    ) -> list[IGDBPlatformResponse] | list[IGDBGenreResponse] | list[IGDBCompanyResponse] | list[IGDBGameResponse]:
        """Run request to the IGDB API.

        Args:
            endpoint (str): The name of the endpoint.
            query (str): The query for the endpoint.
        """
        if not query:
            error_message = "No query provided."
            raise IGDBInteractionError(error_message)
        response = requests.post(
            f"{self.IGDB_BASE_URL}{endpoint}",
            data=query,
            headers=self.basic_auth_headers,
            timeout=10,
        )
        if response.status_code != status.HTTP_200_OK:
            error_message = f"Unable to get the {endpoint}. Response: {response.json()}"
            raise IGDBInteractionError(error_message)
        return self._cast_response(endpoint, response.json())

    def get_all_objects(
        self: Self,
        endpoint: str,
        query: str,
    ) -> list[IGDBPlatformResponse] | list[IGDBGenreResponse] | list[IGDBCompanyResponse] | list[IGDBGameResponse]:
        """Get all objects from the IGDB database.

        Args:
            endpoint (str): The name of the endpoint.
            query (str): The query for the endpoint.
        """
        result: list[IGDBPlatformResponse | IGDBGenreResponse | IGDBCompanyResponse | IGDBGameResponse] = []
        offset = 0
        query = f"{query}limit {self.QUERY_ITEM_LIMIT};sort id;"
        items_in_response = 0
        for response in self.api_multi_request(endpoint, query, offset):
            response_cast = self._cast_response(endpoint, response.json())
            items_in_response += len(response_cast)
            result.extend(response_cast)
        while items_in_response == 4 * self.QUERY_ITEM_LIMIT:
            items_in_response = 0
            offset += 4 * self.QUERY_ITEM_LIMIT
            for response in self.api_multi_request(endpoint, query, offset):
                response_cast = self._cast_response(endpoint, response.json())
                items_in_response += len(response_cast)
                result.extend(response_cast)
            # IGDB API has a limit of 4 requests per second
            time.sleep(1)

        return result

    def api_multi_request(self: Self, endpoint: str, query: str, offset: int = 0) -> list[requests.Response]:
        """Run up to 4 request at the same time to the IGDB API."""
        if not query:
            error_message = "No query provided."
            raise IGDBInteractionError(error_message)
        session = FuturesSession()
        requests = [
            session.post(
                f"{self.IGDB_BASE_URL}{endpoint}",
                data=f"{query}offset {new_offset};sort id;",
                headers=self.basic_auth_headers,
                timeout=10,
            )
            for new_offset in range(offset, offset + (4 * self.QUERY_ITEM_LIMIT), self.QUERY_ITEM_LIMIT)
        ]

        return [req.result() for req in requests]
