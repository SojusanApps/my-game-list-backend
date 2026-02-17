"""This module contains the serializers for the collection related data."""

from typing import Self

from rest_framework import serializers

from my_game_list.collections.models import (
    Collection,
    CollectionItem,
    CollectionMode,
    CollectionType,
    CollectionVisibility,
    Tier,
)
from my_game_list.games.models import Game
from my_game_list.users.models import User
from my_game_list.users.serializers import UserSerializer


class CollectionItemGameSerializer(serializers.ModelSerializer[Game]):
    """A simple serializer for the Game model used in collection items."""

    class Meta:
        """Meta data for the collection item game serializer."""

        model = Game
        fields = ("id", "title", "cover_image_id")


class CollectionItemSerializer(serializers.ModelSerializer[CollectionItem]):
    """A serializer for the collection item model."""

    game = CollectionItemGameSerializer(read_only=True)
    tier_display = serializers.CharField(source="get_tier_display", read_only=True)
    added_by = UserSerializer(read_only=True)

    class Meta:
        """Meta data for the collection item serializer."""

        model = CollectionItem
        fields = (
            "id",
            "order",
            "tier",
            "tier_display",
            "description",
            "created_at",
            "last_modified_at",
            "collection",
            "game",
            "added_by",
        )


class CollectionItemCreateSerializer(serializers.ModelSerializer[CollectionItem]):
    """A serializer for creating collection items."""

    game = serializers.SlugRelatedField(
        queryset=Game.objects.all(),
        slug_field="id",
    )
    tier = serializers.ChoiceField(choices=Tier.choices, required=False, allow_blank=True, default="")

    class Meta:
        """Meta data for the collection item create serializer."""

        model = CollectionItem
        fields = (
            "id",
            "order",
            "tier",
            "description",
            "created_at",
            "last_modified_at",
            "collection",
            "game",
            "added_by",
        )
        read_only_fields = ("added_by", "order")


class CollectionSerializer(serializers.ModelSerializer[Collection]):
    """A serializer for the collection model."""

    visibility_display = serializers.CharField(source="get_visibility_display", read_only=True)
    mode_display = serializers.CharField(source="get_mode_display", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    user = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    items_cover_image_ids = serializers.SerializerMethodField()

    class Meta:
        """Meta data for the collection serializer."""

        model = Collection
        fields = (
            "id",
            "name",
            "description",
            "is_favorite",
            "visibility",
            "visibility_display",
            "mode",
            "mode_display",
            "type",
            "type_display",
            "created_at",
            "last_modified_at",
            "user",
            "collaborators",
            "items_count",
            "items_cover_image_ids",
        )

    def get_items_count(self: Self, instance: Collection) -> int:
        """Get the number of items in the collection."""
        return instance.items.count()

    def get_items_cover_image_ids(self: Self, instance: Collection) -> list[str | None]:
        """Get the first 5 items in the collection.

        Just the cover image IDs for associated games so it could be displayed on the frontend.
        """
        cache = getattr(instance, "_prefetched_objects_cache", None)
        if cache is not None and "items" in cache:
            items_from_cache = sorted(cache["items"], key=lambda x: (x.order, x.id))[:5]
            return [item.game.cover_image_id for item in items_from_cache]

        items = instance.items.select_related("game").order_by("order")[:5]
        return [item.game.cover_image_id for item in items]


class CollectionDetailSerializer(CollectionSerializer):
    """A detailed serializer for the collection model including items."""

    items = CollectionItemSerializer(many=True, read_only=True)

    class Meta(CollectionSerializer.Meta):
        """Meta data for the collection detail serializer."""

        fields = (*CollectionSerializer.Meta.fields, "items")  # type: ignore[assignment]


class CollectionCreateSerializer(serializers.ModelSerializer[Collection]):
    """A serializer for creating collections."""

    visibility = serializers.ChoiceField(
        choices=CollectionVisibility.choices,
        default=CollectionVisibility.PRIVATE,
    )
    mode = serializers.ChoiceField(
        choices=CollectionMode.choices,
        default=CollectionMode.SOLO,
    )
    type = serializers.ChoiceField(
        choices=CollectionType.choices,
        default=CollectionType.NORMAL,
    )
    collaborators = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="id",
        many=True,
        required=False,
    )

    class Meta:
        """Meta data for the collection create serializer."""

        model = Collection
        fields = (
            "id",
            "name",
            "description",
            "is_favorite",
            "visibility",
            "mode",
            "type",
            "created_at",
            "last_modified_at",
            "user",
            "collaborators",
        )
        read_only_fields = ("user",)


class CollectionItemReorderSerializer(serializers.Serializer[CollectionItem]):
    """A serializer for reordering a single collection item."""

    position = serializers.IntegerField(min_value=0)


class CollectionItemTierUpdateSerializer(serializers.Serializer[CollectionItem]):
    """A serializer for updating a collection item's tier."""

    tier = serializers.ChoiceField(choices=Tier.choices, allow_blank=True)
    position = serializers.IntegerField(min_value=0, required=False)


class CollectionItemPositionSerializer(serializers.Serializer[CollectionItem]):
    """A serializer for a single item position entry used in bulk reorder."""

    id = serializers.IntegerField()
    position = serializers.IntegerField(min_value=0)


class CollectionItemBulkReorderSerializer(serializers.Serializer[CollectionItem]):
    """A serializer for bulk-reordering all items in a collection.

    Accepts a list of items with their new positions. This resets the fractional
    ordering system and assigns each item a clean integer order value.

    Expected payload:
    {
        "items": [
            {"id": 5, "position": 0},
            {"id": 3, "position": 1},
            {"id": 7, "position": 2}
        ]
    }
    """

    items = CollectionItemPositionSerializer(many=True)

    def validate_items(
        self: Self,
        value: list[dict[str, int]],
    ) -> list[dict[str, int]]:
        """Validate that there are no duplicate IDs or positions."""
        ids = [entry["id"] for entry in value]
        positions = [entry["position"] for entry in value]

        if len(ids) != len(set(ids)):
            message = "Duplicate item IDs are not allowed."
            raise serializers.ValidationError(message)

        if len(positions) != len(set(positions)):
            message = "Duplicate positions are not allowed."
            raise serializers.ValidationError(message)

        return value
