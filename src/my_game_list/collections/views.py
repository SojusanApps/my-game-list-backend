"""This module contains the viewsets for the collection related data."""

from typing import TYPE_CHECKING, Self

from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.collections.filters import CollectionFilterSet, CollectionItemFilterSet
from my_game_list.collections.models import Collection, CollectionItem, CollectionMode, CollectionVisibility
from my_game_list.collections.permissions import CollectionItemPermission, CollectionPermission
from my_game_list.collections.serializers import (
    CollectionCreateSerializer,
    CollectionDetailSerializer,
    CollectionItemCreateSerializer,
    CollectionItemSerializer,
    CollectionSerializer,
)
from my_game_list.friendships.models import Friendship

if TYPE_CHECKING:
    from django.db.models import QuerySet


class CollectionViewSet(ModelViewSet[Collection]):
    """A ViewSet for the Collection model.

    Permissions:
    - List: Returns own collections + visible collections based on visibility
    - Create: Any authenticated user
    - Retrieve: Based on visibility settings (PUBLIC/FRIENDS/PRIVATE)
    - Update/Delete: Only owner
    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, CollectionPermission)
    filterset_class = CollectionFilterSet

    def get_queryset(self: Self) -> QuerySet[Collection]:
        """Get the queryset filtered by visibility permissions.

        Returns collections that the user can see:
        - Own collections
        - Collections where user is a collaborator
        - Public collections
        - Friends' collections (visibility = FRIENDS)
        """
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            # Anonymous users can only see public collections
            return queryset.filter(visibility=CollectionVisibility.PUBLIC)

        # Get IDs of friends
        friend_ids = Friendship.objects.filter(user=user).values_list("friend_id", flat=True)

        # Filter: own collections OR collaborator OR public OR friends' with FRIENDS visibility
        queryset = queryset.filter(
            Q(user=user)  # Own collections
            | Q(collaborators=user)  # Collaborator
            | Q(visibility=CollectionVisibility.PUBLIC)  # Public collections
            | Q(user_id__in=friend_ids, visibility=CollectionVisibility.FRIENDS),  # Friends' collections
        ).distinct()

        if self.action == "retrieve":
            return queryset.select_related("user").prefetch_related("collaborators", "items", "items__game")
        return queryset.select_related("user").prefetch_related("collaborators")

    def get_serializer_class(
        self: Self,
    ) -> type[CollectionCreateSerializer | CollectionSerializer | CollectionDetailSerializer]:
        """Get the serializer class for the Collection model."""
        if self.action in ["create", "update", "partial_update"]:
            return CollectionCreateSerializer
        if self.action == "retrieve":
            return CollectionDetailSerializer
        return CollectionSerializer

    def perform_create(self: Self, serializer: CollectionCreateSerializer) -> None:  # type: ignore[override]
        """Set the user to the current user when creating a collection."""
        serializer.save(user=self.request.user)


class CollectionItemViewSet(ModelViewSet[CollectionItem]):
    """A ViewSet for the CollectionItem model.

    Permissions:
    - List: Filtered by collection visibility
    - Create/Update/Delete: Owner or collaborator (if COLLABORATIVE mode)
    """

    queryset = CollectionItem.objects.all()
    serializer_class = CollectionItemSerializer
    permission_classes = (IsAuthenticated, CollectionItemPermission)
    filterset_class = CollectionItemFilterSet

    def get_queryset(self: Self) -> QuerySet[CollectionItem]:
        """Get the queryset filtered by collection visibility.

        Users can only see items from collections they can access.
        """
        queryset = super().get_queryset().select_related("collection", "game", "added_by")
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(collection__visibility=CollectionVisibility.PUBLIC)

        # Get IDs of friends
        friend_ids = Friendship.objects.filter(user=user).values_list("friend_id", flat=True)

        # Filter items based on collection visibility
        return queryset.filter(
            Q(collection__user=user)  # Own collections
            | Q(collection__collaborators=user)  # Collaborator
            | Q(collection__visibility=CollectionVisibility.PUBLIC)  # Public
            | Q(collection__user_id__in=friend_ids, collection__visibility=CollectionVisibility.FRIENDS),
        ).distinct()

    def get_serializer_class(
        self: Self,
    ) -> type[CollectionItemCreateSerializer | CollectionItemSerializer]:
        """Get the serializer class for the CollectionItem model."""
        if self.action in ["create", "update", "partial_update"]:
            return CollectionItemCreateSerializer
        return CollectionItemSerializer

    def perform_create(self: Self, serializer: CollectionItemCreateSerializer) -> None:  # type: ignore[override]
        """Set the added_by to the current user and validate collection permissions."""
        collection = serializer.validated_data.get("collection")

        # Check if user can add items to this collection
        if collection.user != self.request.user:
            if collection.mode != CollectionMode.COLLABORATIVE:
                message = "Only the owner can add items to non-collaborative collections."
                raise PermissionDenied(message)
            if not collection.collaborators.filter(id=self.request.user.id).exists():
                message = "You must be a collaborator to add items to this collection."
                raise PermissionDenied(message)

        serializer.save(added_by=self.request.user)
