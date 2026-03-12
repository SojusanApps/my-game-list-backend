"""This module contains the viewsets for the game related data."""

from typing import TYPE_CHECKING, Self

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from my_game_list.games.filters import (
    CompanyFilterSet,
    GameEngineFilterSet,
    GameFilterSet,
    GameFollowFilterSet,
    GameListFilterSet,
    GameMediaFilterSet,
    GameModeFilterSet,
    GameReviewFilterSet,
    GameStatusFilterSet,
    GameTypeFilterSet,
    GenreFilterSet,
    PlatformFilterSet,
    PlayerPerspectiveFilterSet,
)
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
from my_game_list.games.serializers import (
    CompanyDetailSerializer,
    CompanySerializer,
    GameCreateSerializer,
    GameEngineSerializer,
    GameFollowSerializer,
    GameListCreateSerializer,
    GameListSerializer,
    GameMediaSerializer,
    GameModeSerializer,
    GameReviewCreateSerializer,
    GameReviewSerializer,
    GameSerializer,
    GameSimpleListSerializer,
    GameStatusSerializer,
    GameTypeSerializer,
    GenreSerializer,
    PlatformSerializer,
    PlayerPerspectiveSerializer,
    ReleaseCalendarQuerySerializer,
)
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly

if TYPE_CHECKING:
    import datetime

    from django.db.models import QuerySet
    from rest_framework.request import Request


HIGHEST_NUMBER_OF_DAYS_IN_MONTH = 31
MAX_GAMES_PER_DAY_IN_CALENDAR = 2


class CompanyViewSet(ModelViewSet[Company]):
    """A ViewSet for the Company model."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = CompanyFilterSet

    def get_queryset(self: Self) -> QuerySet[Company]:
        """Get the queryset for the Company model."""
        queryset = super().get_queryset()
        if self.action == "retrieve":
            return queryset.prefetch_related("games_published", "games_developed")
        return queryset

    def get_serializer_class(
        self: Self,
    ) -> type[CompanySerializer | CompanyDetailSerializer]:
        """Get the serializer class for the Company model."""
        return CompanyDetailSerializer if self.action == "retrieve" else CompanySerializer


class GameFollowViewSet(ModelViewSet[GameFollow]):
    """A ViewSet for the GameFollow model."""

    queryset = GameFollow.objects.all()
    serializer_class = GameFollowSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameFollowFilterSet


class GameListViewSet(ModelViewSet[GameList]):
    """A ViewSet for the GameList model."""

    queryset = GameList.objects.all()
    serializer_class = GameListSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameListFilterSet

    def get_serializer_class(
        self: Self,
    ) -> type[GameListCreateSerializer | GameListSerializer]:
        """Get the serializer class for the Game model."""
        return (
            GameListCreateSerializer
            if self.action
            in [
                "create",
                "update",
                "partial_update",
            ]
            else GameListSerializer
        )

    @action(detail=False, methods=["get"], url_path="random-ptp")
    def random_ptp(self: Self, request: Request) -> Response:
        """Return a random game from the user's game list in status Plan To Play."""
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ptp_game = (
            self.get_queryset()
            .filter(user_id=request.user.pk, status=GameListStatus.PLAN_TO_PLAY)
            .order_by("?")
            .first()
        )
        if not ptp_game:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(ptp_game)
        return Response(serializer.data)


class GameReviewViewSet(ModelViewSet[GameReview]):
    """A ViewSet for the GameReview model."""

    queryset = GameReview.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = GameReviewFilterSet

    def get_serializer_class(
        self: Self,
    ) -> type[GameReviewCreateSerializer | GameReviewSerializer]:
        """Get the serializer class for the Game model."""
        return (
            GameReviewCreateSerializer
            if self.action
            in [
                "create",
                "update",
                "partial_update",
            ]
            else GameReviewSerializer
        )


class GameViewSet(ModelViewSet[Game]):
    """A ViewSet for the Game model."""

    queryset = Game.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameFilterSet

    def get_queryset(self: Self) -> QuerySet[Game]:
        """Get the queryset for the Game model."""
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.select_related("stats", "game_status", "game_type")

        return queryset.select_related(
            "stats",
            "publisher",
            "developer",
            "game_status",
            "game_type",
            "parent_game",
        ).prefetch_related(
            "genres",
            "platforms",
            "bundles",
            "dlcs",
            "expanded_games",
            "expansions",
            "forks",
            "ports",
            "standalone_expansions",
            "game_engines",
            "game_modes",
            "player_perspectives",
        )

    def get_serializer_class(
        self: Self,
    ) -> type[GameCreateSerializer | GameSerializer | GameSimpleListSerializer]:
        """Get the serializer class for the Game model."""
        if self.action in ["create", "update", "partial_update"]:
            return GameCreateSerializer
        if self.action in ("list", "release_calendar"):
            return GameSimpleListSerializer
        return GameSerializer

    @extend_schema(
        request=None,
        parameters=[ReleaseCalendarQuerySerializer],
        responses={200: GameSimpleListSerializer(many=True), 400: None},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="release-calendar",
        pagination_class=None,
        filter_backends=[],
    )
    def release_calendar(self: Self, request: Request) -> Response:
        """Get the game release calendar data."""
        query_serializer = ReleaseCalendarQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        start_date = query_serializer.validated_data.get("start_date")
        end_date = query_serializer.validated_data.get("end_date")

        delta = end_date - start_date
        if delta.days < 0 or delta.days > HIGHEST_NUMBER_OF_DAYS_IN_MONTH:
            return Response(
                {"detail": f"The date range must be between 0 and {HIGHEST_NUMBER_OF_DAYS_IN_MONTH} days."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = (
            self.get_queryset()
            .filter(release_date__range=(start_date, end_date))
            .order_by("release_date", "-stats__popularity")
        )

        grouped_games: dict[datetime.date, list[Game]] = {}
        for game in queryset:
            release_date = game.release_date
            if release_date is None:
                continue

            if release_date not in grouped_games:
                grouped_games[release_date] = []

            if len(grouped_games[release_date]) < MAX_GAMES_PER_DAY_IN_CALENDAR:
                grouped_games[release_date].append(game)

        final_games = []
        for date_games in grouped_games.values():
            final_games.extend(date_games)

        serializer = self.get_serializer(final_games, many=True)
        return Response(serializer.data)


class GenreViewSet(ReadOnlyModelViewSet[Genre]):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GenreFilterSet


class PlatformViewSet(ReadOnlyModelViewSet[Platform]):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlatformFilterSet


class GameTypeViewSet(ReadOnlyModelViewSet[GameType]):
    """A ViewSet for the GameType model."""

    queryset = GameType.objects.all()
    serializer_class = GameTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameTypeFilterSet


class GameStatusViewSet(ReadOnlyModelViewSet[GameStatus]):
    """A ViewSet for the GameStatus model."""

    queryset = GameStatus.objects.all()
    serializer_class = GameStatusSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameStatusFilterSet


class GameEngineViewSet(ReadOnlyModelViewSet[GameEngine]):
    """A ViewSet for the GameEngine model."""

    queryset = GameEngine.objects.all()
    serializer_class = GameEngineSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameEngineFilterSet


class GameModeViewSet(ReadOnlyModelViewSet[GameMode]):
    """A ViewSet for the GameMode model."""

    queryset = GameMode.objects.all()
    serializer_class = GameModeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameModeFilterSet


class PlayerPerspectiveViewSet(ReadOnlyModelViewSet[PlayerPerspective]):
    """A ViewSet for the PlayerPerspective model."""

    queryset = PlayerPerspective.objects.all()
    serializer_class = PlayerPerspectiveSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlayerPerspectiveFilterSet


class GameMediaViewSet(ModelViewSet[GameMedia]):
    """A ViewSet for the GameMedia model."""

    queryset = GameMedia.objects.all()
    serializer_class = GameMediaSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameMediaFilterSet
