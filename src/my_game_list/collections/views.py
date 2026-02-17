"""This module contains the viewsets for the collection related data."""

from decimal import Decimal
from typing import TYPE_CHECKING, Self

from django.db.models import F, Max, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.collections.filters import CollectionFilterSet, CollectionItemFilterSet
from my_game_list.collections.models import Collection, CollectionItem, CollectionMode, CollectionVisibility
from my_game_list.collections.permissions import (
    CollectionItemPermission,
    CollectionPermission,
    IsCollectionOwnerOrCollaborator,
)
from my_game_list.collections.serializers import (
    CollectionCreateSerializer,
    CollectionDetailSerializer,
    CollectionItemCreateSerializer,
    CollectionItemReorderSerializer,
    CollectionItemSerializer,
    CollectionItemTierUpdateSerializer,
    CollectionSerializer,
)
from my_game_list.friendships.models import Friendship

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request


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

    def _calculate_fractional_order(
        self: Self,
        collection: Collection,
        position: int,
        tier: str = "",
        exclude_item: CollectionItem | None = None,
    ) -> Decimal:
        """Calculate fractional order for an item at the given position.

        Args:
            collection: The collection containing the items
            position: The target position (0-based index)
            tier: The tier to calculate order within (empty string for non-tier lists)
            exclude_item: Item to exclude from calculation (when reordering an existing item)

        Returns:
            Decimal: The calculated fractional order value
        """
        items = CollectionItem.objects.filter(
            collection=collection,
            tier=tier,
        )

        # Exclude the item being moved to get the correct target position
        if exclude_item:
            items = items.exclude(id=exclude_item.id)

        items = items.order_by("order", "id")

        items_list = list(items)
        total_items = len(items_list)

        # Position at beginning
        if position == 0:
            if total_items == 0:
                return Decimal("1.0")
            first_order = items_list[0].order or Decimal("1.0")
            return first_order / Decimal("2.0")

        # Position at or beyond end
        if position >= total_items:
            if total_items == 0:
                return Decimal("1.0")
            last_order = items_list[-1].order or Decimal("1.0")
            return last_order + Decimal("1.0")

        # Position in the middle - between two items
        prev_item = items_list[position - 1]
        next_item = items_list[position]

        prev_order = prev_item.order or Decimal("1.0")
        next_order = next_item.order or Decimal("2.0")

        # If orders are equal (e.g., due to data inconsistencies), avoid returning
        # a duplicate midpoint by falling back to appending at the end.
        if prev_order == next_order:
            last_order = items_list[-1].order or Decimal("1.0")
            return last_order + Decimal("1.0")

        # Calculate midpoint
        return (prev_order + next_order) / Decimal("2.0")

    @action(
        detail=True,
        methods=["post"],
        url_path="items/(?P<item_id>[^/.]+)/reorder",
        permission_classes=[IsAuthenticated, IsCollectionOwnerOrCollaborator],
    )
    def reorder_item(
        self: Self,
        request: Request,
        pk: str | None = None,  # noqa: ARG002
        item_id: str | None = None,
    ) -> Response:
        """Reorder a single item in the collection using fractional indexing.

        The backend calculates the fractional order based on the target position
        and its neighbors. This allows inserting items without renumbering others.

        Args:
            request: The HTTP request containing position data
            pk: Collection ID (from URL)
            item_id: ID of the item to reorder (from URL)

        Expected payload:
        {
            "position": 2  # 0-based index of the new position within the same tier
        }
        """
        collection = self.get_object()
        serializer = CollectionItemReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        position = serializer.validated_data["position"]

        # Get the item to reorder
        try:
            item = CollectionItem.objects.get(id=int(item_id) if item_id else 0, collection=collection)
        except CollectionItem.DoesNotExist:
            return Response(
                {"detail": f"Item with ID {item_id} not found in this collection."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Calculate new fractional order based on position and neighbors
        new_order = self._calculate_fractional_order(collection, position, tier=item.tier, exclude_item=item)

        # Update the item's order
        item.order = new_order
        item.save(update_fields=["order"])

        return Response({"order": str(new_order)}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="items/(?P<item_id>[^/.]+)/update-tier",
        permission_classes=[IsAuthenticated, IsCollectionOwnerOrCollaborator],
    )
    def update_tier(
        self: Self,
        request: Request,
        pk: str | None = None,  # noqa: ARG002
        item_id: str | None = None,
    ) -> Response:
        """Update tier and optionally position for a single item.

        When changing tiers, you can optionally specify a new position within that tier.
        If no position is provided, the item will be placed at the end of the new tier.

        Args:
            request: The HTTP request containing tier and optional position data
            pk: Collection ID (from URL)
            item_id: ID of the item to update (from URL)

        Expected payload:
        {
            "tier": "S",
            "position": 1  # Optional
        }
        """
        collection = self.get_object()
        serializer = CollectionItemTierUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tier = serializer.validated_data["tier"]
        position = serializer.validated_data.get("position")

        # Get the item to update
        try:
            item = CollectionItem.objects.get(id=int(item_id) if item_id else 0, collection=collection)
        except CollectionItem.DoesNotExist:
            return Response(
                {"detail": f"Item with ID {item_id} not found in this collection."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update tier
        item.tier = tier

        # Calculate new order if position is provided, otherwise append to end
        if position is not None:
            new_order = self._calculate_fractional_order(collection, position, tier=tier, exclude_item=item)
        else:
            # Append to end of new tier
            max_order = CollectionItem.objects.filter(
                collection=collection,
                tier=tier,
            ).aggregate(
                Max("order"),
            )["order__max"]
            new_order = (Decimal(str(max_order)) if max_order else Decimal("0.0")) + Decimal("1.0")

        item.order = new_order
        item.save(update_fields=["tier", "order"])

        return Response({"tier": tier, "order": str(new_order)}, status=status.HTTP_200_OK)


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
        Items are ordered by the 'order' field (ascending, lowest first).
        """
        queryset = super().get_queryset().select_related("collection", "game", "added_by")
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(collection__visibility=CollectionVisibility.PUBLIC).order_by(
                F("order").asc(nulls_last=True),
            )

        # Get IDs of friends
        friend_ids = Friendship.objects.filter(user=user).values_list("friend_id", flat=True)

        # Filter items based on collection visibility
        return (
            queryset.filter(
                Q(collection__user=user)  # Own collections
                | Q(collection__collaborators=user)  # Collaborator
                | Q(collection__visibility=CollectionVisibility.PUBLIC)  # Public
                | Q(collection__user_id__in=friend_ids, collection__visibility=CollectionVisibility.FRIENDS),
            )
            .distinct()
            .order_by(F("order").asc(nulls_last=True))
        )

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

        # Calculate order using fractional indexing for items with empty tier
        max_order = CollectionItem.objects.filter(
            collection=collection,
            tier=serializer.validated_data.get("tier", ""),
        ).aggregate(Max("order"))["order__max"]

        next_order = Decimal("1.0") if max_order is None else Decimal(str(max_order)) + Decimal("1.0")

        serializer.save(added_by=self.request.user, order=next_order)
