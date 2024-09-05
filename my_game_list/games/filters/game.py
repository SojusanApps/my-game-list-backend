"""Filters for game model."""

from django_filters import rest_framework as filters

from my_game_list.games.models import Game, Genre, Platform


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
            ("rank_position", "rank_position"),
            ("popularity", "popularity"),
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
