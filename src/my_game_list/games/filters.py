"""Filters for game related data."""

from django_filters import rest_framework as filters

from my_game_list.games.models import (
    Company,
    Game,
    GameEngine,
    GameFollow,
    GameList,
    GameListStatus,
    GameMedia,
    GameMode,
    GameReview,
    GameStatus,
    GameType,
    Genre,
    Platform,
    PlayerPerspective,
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
    game_type = filters.ModelMultipleChoiceFilter(
        field_name="game_type__type",
        to_field_name="type",
        queryset=GameType.objects.all(),
    )
    game_status = filters.ModelMultipleChoiceFilter(
        field_name="game_status__status",
        to_field_name="status",
        queryset=GameStatus.objects.all(),
    )
    game_engines = filters.ModelMultipleChoiceFilter(
        field_name="game_engines__name",
        to_field_name="name",
        queryset=GameEngine.objects.all(),
    )
    game_modes = filters.ModelMultipleChoiceFilter(
        field_name="game_modes__name",
        to_field_name="name",
        queryset=GameMode.objects.all(),
    )
    player_perspectives = filters.ModelMultipleChoiceFilter(
        field_name="player_perspectives__name",
        to_field_name="name",
        queryset=PlayerPerspective.objects.all(),
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
            "game_type",
            "game_status",
            "game_engines",
            "game_modes",
            "player_perspectives",
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


class GameTypeFilterSet(filters.FilterSet):
    """Filter set for game type model."""

    type = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        """Meta class for GameTypeFilterSet."""

        model = GameType
        fields = ("id", "type", "igdb_id")


class GameStatusFilterSet(filters.FilterSet):
    """Filter set for game status model."""

    status = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        """Meta class for GameStatusFilterSet."""

        model = GameStatus
        fields = ("id", "status", "igdb_id")


class GameEngineFilterSet(BaseDictionaryFilterSet):
    """Filter set for game engine model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GameEngineFilterSet."""

        model = GameEngine
        fields = (*BaseDictionaryFilterSet.Meta.fields, "igdb_id")


class GameModeFilterSet(BaseDictionaryFilterSet):
    """Filter set for game mode model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GameModeFilterSet."""

        model = GameMode
        fields = (*BaseDictionaryFilterSet.Meta.fields, "igdb_id")


class PlayerPerspectiveFilterSet(BaseDictionaryFilterSet):
    """Filter set for player perspective model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for PlayerPerspectiveFilterSet."""

        model = PlayerPerspective
        fields = (*BaseDictionaryFilterSet.Meta.fields, "igdb_id")


class GameMediaFilterSet(BaseDictionaryFilterSet):
    """Filter set for game media model."""

    class Meta(BaseDictionaryFilterSet.Meta):
        """Meta class for GameMediaFilterSet."""

        model = GameMedia
