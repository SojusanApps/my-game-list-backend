"""FilterSet for friendship request model."""

from django_filters import rest_framework as filters

from my_game_list.friendships.models import FriendshipRequest


class FriendshipRequestFilterSet(filters.FilterSet):
    """FilterSet for friendship request model."""

    sender = filters.NumberFilter(field_name="sender__id")
    receiver = filters.NumberFilter(field_name="receiver__id")

    class Meta:
        """Meta class for friendship request model."""

        model = FriendshipRequest
        fields = (
            "id",
            "sender",
            "receiver",
        )
