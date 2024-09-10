"""Filters for game follow model."""

from django_filters import rest_framework as filters

from my_game_list.games.models import GameFollow


class GameFollowFilterSet(filters.FilterSet):
    """FilterSet for game follow model."""

    game = filters.NumberFilter(field_name="game__id")
    user = filters.NumberFilter(field_name="user_id")

    class Meta:
        """Meta class for game follow filter set."""

        model = GameFollow
        fields = (
            "id",
            "game",
            "user",
        )
