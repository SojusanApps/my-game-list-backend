"""Filters for game related data."""

from django_filters import rest_framework as filters

from my_game_list.games.models import (
    Company,
    Game,
    GameFollow,
    GameList,
    GameListStatus,
    GameMedia,
    GameReview,
    Genre,
    Platform,
)
from my_game_list.my_game_list.filters import BaseDictionaryFilterSet


class CompanyFilterSet(BaseDictionaryFilterSet):
    """Filter set for company model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for CompanyFilterSet."""

        model = Company
        fields: tuple[str, ...] = (*BaseDictionaryFilterSet.Meta.fields, "igdb_id")


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


class GameFilterSet(filters.FilterSet):
    """FilterSet for game model."""

    title = filters.CharFilter(lookup_expr="icontains")
    release_date = filters.DateFromToRangeFilter()
    publisher = filters.CharFilter(field_name="publisher__name", lookup_expr="icontains")
    developer = filters.CharFilter(field_name="developer__name", lookup_expr="icontains")
    genres = filters.ModelMultipleChoiceFilter(
        field_name="genres__name",
        to_field_name="name",
        queryset=Genre.objects.all(),
    )
    platforms = filters.ModelMultipleChoiceFilter(
        field_name="platforms__name",
        to_field_name="name",
        queryset=Platform.objects.all(),
    )
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("stats__rank_position", "rank_position"),
            ("stats__popularity", "popularity"),
        ),
    )

    class Meta:
        """Meta class for GameFilterSet."""

        model = Game
        fields = (
            "id",
            "title",
            "release_date",
            "publisher",
            "developer",
            "genres",
            "platforms",
        )


class GenreFilterSet(BaseDictionaryFilterSet):
    """Filter set for genre model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GenreFilterSet."""

        model = Genre


class PlatformFilterSet(BaseDictionaryFilterSet):
    """Filter set for platform model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for PlatformFilterSet."""

        model = Platform


class GameMediaFilterSet(BaseDictionaryFilterSet):
    """Filter set for game media model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GameMediaFilterSet."""

        model = GameMedia
