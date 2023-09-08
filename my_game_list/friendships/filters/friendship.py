"""FilterSet for friendship model."""
from django_filters import rest_framework as filters

from my_game_list.friendships.models import Friendship


class FriendshipFilterSet(filters.FilterSet):
    """FilterSet for friendship model."""

    user = filters.NumberFilter(field_name="user__id")

    class Meta:
        """Meta class for friendship filter set."""

        model = Friendship
        fields = (
            "id",
            "user",
        )
