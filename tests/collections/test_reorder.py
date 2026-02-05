"""Tests for the Collection reorder items endpoint."""

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from my_game_list.collections.models import Collection, CollectionItem
    from my_game_list.users.models import User

# Named constants to avoid magic numbers in tests
REORDER_ORDER_1 = 10
REORDER_ORDER_2 = 20
COLLAB_ORDER = 5


@pytest.mark.django_db()
class TestCollectionReorderItems:
    """Tests for the reorder-items action in CollectionViewSet."""

    def test_reorder_items_success(
        self,
        authenticated_api_client: APIClient,
        user_fixture: User,
    ) -> None:
        """Test successfully reordering items in a collection."""
        collection: Collection = baker.make("collections.Collection", user=user_fixture)
        item1: CollectionItem = baker.make("collections.CollectionItem", collection=collection, order=1)
        item2: CollectionItem = baker.make("collections.CollectionItem", collection=collection, order=2)

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        data = [
            {"id": item1.id, "order": REORDER_ORDER_1},
            {"id": item2.id, "order": REORDER_ORDER_2},
        ]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        item1.refresh_from_db()
        item2.refresh_from_db()
        assert item1.order == REORDER_ORDER_1
        assert item2.order == REORDER_ORDER_2

    def test_reorder_items_not_owner(
        self,
        authenticated_api_client: APIClient,
    ) -> None:
        """Test that a non-owner cannot reorder items in a private collection."""
        other_user: User = baker.make("users.User")
        collection: Collection = baker.make("collections.Collection", user=other_user, visibility="PRI")
        item: CollectionItem = baker.make("collections.CollectionItem", collection=collection, order=1)

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        data = [{"id": item.id, "order": REORDER_ORDER_1}]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND  # Because get_queryset filters it out

    def test_reorder_items_invalid_id(
        self,
        authenticated_api_client: APIClient,
        user_fixture: User,
    ) -> None:
        """Test reordering with an item ID that doesn't belong to the collection."""
        collection: Collection = baker.make("collections.Collection", user=user_fixture)
        other_item: CollectionItem = baker.make("collections.CollectionItem")

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        data = [{"id": other_item.id, "order": 10}]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not found in this collection" in response.data["detail"]

    def test_reorder_items_collaborative(
        self,
        authenticated_api_client: APIClient,
        user_fixture: User,
    ) -> None:
        """Test that a collaborator can reorder items in a collaborative collection."""
        owner: User = baker.make("users.User")
        collection: Collection = baker.make(
            "collections.Collection",
            user=owner,
            mode="C",  # COLLABORATIVE
            visibility="PUB",
        )
        collection.collaborators.add(user_fixture)
        item: CollectionItem = baker.make("collections.CollectionItem", collection=collection, order=1)

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        data = [{"id": item.id, "order": COLLAB_ORDER}]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        item.refresh_from_db()
        assert item.order == COLLAB_ORDER

    def test_reorder_items_with_description(
        self,
        authenticated_api_client: APIClient,
        user_fixture: User,
    ) -> None:
        """Test successfully reordering items and updating description."""
        collection: Collection = baker.make("collections.Collection", user=user_fixture)
        item: CollectionItem = baker.make(
            "collections.CollectionItem",
            collection=collection,
            order=1,
            description="old description",
        )

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        new_description = "new description"
        data = [{"id": item.id, "order": REORDER_ORDER_1, "description": new_description}]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        item.refresh_from_db()
        assert item.order == REORDER_ORDER_1
        assert item.description == new_description

    def test_reorder_items_description_optional(
        self,
        authenticated_api_client: APIClient,
        user_fixture: User,
    ) -> None:
        """Test that description is optional and not cleared if not provided."""
        collection: Collection = baker.make("collections.Collection", user=user_fixture)
        initial_description = "keep me"
        item: CollectionItem = baker.make(
            "collections.CollectionItem",
            collection=collection,
            order=1,
            description=initial_description,
        )

        url = reverse("collections:collections-reorder-items", kwargs={"pk": collection.pk})
        data = [{"id": item.id, "order": REORDER_ORDER_2}]

        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        item.refresh_from_db()
        assert item.order == REORDER_ORDER_2
        assert item.description == initial_description
