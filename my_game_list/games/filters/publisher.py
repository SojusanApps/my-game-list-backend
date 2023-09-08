"""Filters for publisher model."""
from my_game_list.games.models import Publisher
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class PublisherFilterSet(BaseDictionaryFilterSet):
    """Filter set for publisher model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for PublisherFilterSet."""

        model = Publisher
