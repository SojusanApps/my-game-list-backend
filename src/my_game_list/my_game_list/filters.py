"""Base filters for dictionary models."""

from django_filters import rest_framework as filters


class BaseDictionaryFilterSet(filters.FilterSet):
    """Filter set for base dictionary models."""

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        """Meta class for BaseDictionaryFilterSet."""

        fields: tuple[str, ...] = ("id", "name")
