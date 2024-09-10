"""Filters for game review model."""

from django_filters import rest_framework as filters

from my_game_list.games.models import GameReview


class GameReviewFilterSet(filters.FilterSet):
    """FilterSet for game review model."""

    score = filters.NumberFilter()
    game = filters.NumberFilter(field_name="game__id")
    user = filters.NumberFilter(field_name="user__id")

    class Meta:
        """Meta class for game review filter set."""

        model = GameReview
        fields = (
            "id",
            "score",
            "game",
            "user",
        )
