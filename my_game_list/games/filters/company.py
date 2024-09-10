"""Filters for company model."""

from my_game_list.games.models import Company
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class CompanyFilterSet(BaseDictionaryFilterSet):
    """Filter set for company model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for CompanyFilterSet."""

        model = Company
        fields: tuple[str, ...] = (*BaseDictionaryFilterSet.Meta.fields, "igdb_id")
