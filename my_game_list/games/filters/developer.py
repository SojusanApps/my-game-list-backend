"""Filters for developer model."""
from my_game_list.games.models import Developer
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class DeveloperFilterSet(BaseDictionaryFilterSet):
    """Filter set for developer model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for DeveloperFilterSet."""

        model = Developer
