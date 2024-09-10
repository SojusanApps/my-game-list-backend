"""Filters for game list model."""

from django_filters import rest_framework as filters

from my_game_list.games.models import GameList, GameListStatus


class GameListFilterSet(filters.FilterSet):
    """FilterSet for game list model."""

    status = filters.MultipleChoiceFilter(choices=GameListStatus.choices)
    game = filters.NumberFilter(field_name="game__id")
    user = filters.NumberFilter(field_name="user__id")

    class Meta:
        """Meta class for game list filter set."""

        model = GameList
        fields = (
            "id",
            "status",
            "game",
            "user",
        )
