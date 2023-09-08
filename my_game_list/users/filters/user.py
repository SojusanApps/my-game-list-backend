"""Filters for user model."""
from django_filters import rest_framework as filters

from my_game_list.users.models import User


class UserFilterSet(filters.FilterSet):
    """FilterSet for user model."""

    username = filters.CharFilter(lookup_expr="icontains")
    is_active = filters.BooleanFilter()

    class Meta:
        """Meta class for user filter set."""

        model = User
        fields = (
            "id",
            "username",
            "is_active",
        )
