"""Filters for platform model."""
from my_game_list.games.models import Platform
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class PlatformFilterSet(BaseDictionaryFilterSet):
    """Filter set for platform model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for PlatformFilterSet."""

        model = Platform
