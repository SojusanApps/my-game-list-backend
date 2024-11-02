"""The queryset for the game related data."""

from typing import TYPE_CHECKING, Self

from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, QuerySet, Window
from django.db.models.functions import Coalesce, Round, RowNumber

if TYPE_CHECKING:
    from my_game_list.games.models import Game  # noqa: F401


class GameQuerySet(QuerySet["Game"]):
    """The queryset for the Game model."""

    def with_scores_count(self: Self) -> Self:
        """Annotate the number of all ratings for the game."""
        return self.annotate(scores_count=Count("game_lists__score"))

    def with_average_score(self: Self) -> Self:
        """Annotate the average score for the game."""
        return self.annotate(
            average_score=Coalesce(
                ExpressionWrapper(
                    Round(Avg("game_lists__score"), 2),
                    output_field=DecimalField(max_digits=4, decimal_places=2),
                ),
                0,
                output_field=DecimalField(max_digits=4, decimal_places=2),
            ),
        )

    def with_members_count(self: Self) -> Self:
        """Annotate the number of all members for the game."""
        return self.annotate(members_count=Count("game_lists"))

    def with_popularity(self: Self) -> Self:
        """Annotate the popularity of the game. The popularity is calculated based on the number of members."""
        return self.with_members_count().annotate(popularity=Window(expression=RowNumber(), order_by="-members_count"))

    def with_rank_position(self: Self) -> Self:
        """Annotate the rank position of the game. The rank position is calculated based on the average score."""
        return self.with_average_score().annotate(
            rank_position=Window(expression=RowNumber(), order_by="-average_score"),
        )
