"""Filters for genre model."""
from my_game_list.games.models import Genre
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class GenreFilterSet(BaseDictionaryFilterSet):
    """Filter set for genre model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GenreFilterSet."""

        model = Genre
