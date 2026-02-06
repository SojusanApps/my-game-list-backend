"""Filters for collection related data."""

from django_filters import rest_framework as filters

from my_game_list.collections.models import Collection, CollectionItem, CollectionMode, CollectionVisibility, Tier


class CollectionFilterSet(filters.FilterSet):
    """FilterSet for collection model."""

    name = filters.CharFilter(lookup_expr="icontains")
    user = filters.NumberFilter(field_name="user__id")
    visibility = filters.MultipleChoiceFilter(choices=CollectionVisibility.choices)
    mode = filters.MultipleChoiceFilter(choices=CollectionMode.choices)
    is_favorite = filters.BooleanFilter()
    collaborator = filters.NumberFilter(field_name="collaborators__id")

    class Meta:
        """Meta class for collection filter set."""

        model = Collection
        fields = (
            "id",
            "name",
            "user",
            "visibility",
            "mode",
            "is_favorite",
            "collaborator",
        )


class CollectionItemFilterSet(filters.FilterSet):
    """FilterSet for collection item model."""

    collection = filters.NumberFilter(field_name="collection__id")
    game = filters.NumberFilter(field_name="game__id")
    tier = filters.MultipleChoiceFilter(choices=Tier.choices)
    added_by = filters.NumberFilter(field_name="added_by__id")

    ordering = filters.OrderingFilter(
        fields=(
            ("order", "order"),
            ("created_at", "created_at"),
            ("tier", "tier"),
        ),
    )

    class Meta:
        """Meta class for collection item filter set."""

        model = CollectionItem
        fields = (
            "id",
            "collection",
            "game",
            "tier",
            "added_by",
        )
