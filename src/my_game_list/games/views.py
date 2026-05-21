"""This module contains the viewsets for the game related data."""

from typing import TYPE_CHECKING, Self

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from my_game_list.games.filters import (
    CompanyFilterSet,
    ExternalGameSourceFilterSet,
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
    ExternalGameSource,
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
    ExternalGameSourceSerializer,
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
MAX_GAMES_PER_DAY_IN_CALENDAR = 3


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all companies in the catalogue. "
            "Companies are read-only Dictionary Model entries that represent both publishers "
            "and developers. Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact company ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by company name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the company's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description=(
            "Retrieve a single company by ID. "
            "The detail response includes the lists of games the company has published and developed."
        ),
    ),
)
class CompanyViewSet(ReadOnlyModelViewSet[Company]):
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


@extend_schema_view(
    list=extend_schema(
        description=(
            "List game-follow records. "
            "A game follow records that a user is tracking a game to receive updates. "
            "Filter by game or user ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game-follow record ID.",
            ),
            OpenApiParameter(
                name="game",
                description="Filter by game ID.",
            ),
            OpenApiParameter(
                name="user",
                description="Filter by user ID.",
            ),
        ],
    ),
    create=extend_schema(
        description="Follow a game. Creates a record linking the authenticated user to the specified game.",
    ),
    retrieve=extend_schema(
        description="Retrieve a single game-follow record by ID.",
    ),
    update=extend_schema(
        description="Replace all fields of a game-follow record.",
    ),
    partial_update=extend_schema(
        description="Update one or more fields of a game-follow record.",
    ),
    destroy=extend_schema(
        description="Unfollow a game. Removes the follow record permanently.",
    ),
)
class GameFollowViewSet(ModelViewSet[GameFollow]):
    """A ViewSet for the GameFollow model."""

    queryset = GameFollow.objects.all()
    serializer_class = GameFollowSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = GameFollowFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List game-list entries for the authenticated user. "
            "Each entry tracks a user's relationship to a game including the play status "
            "(e.g. Playing, Completed, Plan to Play). "
            "Filter by status, game ID, or user ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game-list entry ID.",
            ),
            OpenApiParameter(
                name="status",
                description=("Filter by play status. Can be specified multiple times to match several statuses."),
            ),
            OpenApiParameter(
                name="game",
                description="Filter by game ID.",
            ),
            OpenApiParameter(
                name="user",
                description="Filter by user ID.",
            ),
        ],
    ),
    create=extend_schema(
        description="Add a game to the authenticated user's game list with the specified play status.",
    ),
    retrieve=extend_schema(
        description="Retrieve a single game-list entry by ID.",
    ),
    update=extend_schema(
        description="Replace all fields of a game-list entry.",
    ),
    partial_update=extend_schema(
        description="Update one or more fields of a game-list entry, for example to change the play status.",
    ),
    destroy=extend_schema(
        description="Remove a game-list entry. This does not delete the underlying game record.",
    ),
)
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

    @extend_schema(
        description=(
            "Return a random game from the authenticated user's game list that has status "
            "Plan to Play. Returns HTTP 404 if the user has no Plan to Play games. "
            "Use this endpoint to get a suggestion for what to play next."
        ),
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


@extend_schema_view(
    list=extend_schema(
        description=(
            "List game reviews. "
            "Each review contains a numeric score and an optional text body submitted by a user. "
            "Filter by score, game ID, or reviewer user ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game review ID.",
            ),
            OpenApiParameter(
                name="score",
                description="Filter by exact review score.",
            ),
            OpenApiParameter(
                name="game",
                description="Filter by game ID.",
            ),
            OpenApiParameter(
                name="user",
                description="Filter by reviewer user ID.",
            ),
        ],
    ),
    create=extend_schema(
        description="Submit a review for a game. The authenticated user is recorded as the reviewer.",
    ),
    retrieve=extend_schema(
        description="Retrieve a single game review by ID.",
    ),
    update=extend_schema(
        description="Replace all fields of an existing game review.",
    ),
    partial_update=extend_schema(
        description="Update one or more fields of a game review, for example to revise the score or text.",
    ),
    destroy=extend_schema(
        description="Delete a game review permanently.",
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        description=(
            "List games in the catalogue. "
            "The `title` filter searches across both the English (`title_en`) and Polish "
            "(`title_pl`) title fields simultaneously. "
            "Results can be ordered by `rank_position`, `popularity`, `release_date`, "
            "or `created_at` using the `ordering` parameter."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game ID.",
            ),
            OpenApiParameter(
                name="title",
                description=(
                    "Search by game title. Searches both the English and Polish title fields "
                    "simultaneously (case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="release_date_after",
                description="Filter games with a release date on or after this date (YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="release_date_before",
                description="Filter games with a release date on or before this date (YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="publisher",
                description=(
                    "Filter by publisher name. Searches both English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="developer",
                description=(
                    "Filter by developer name. Searches both English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="genres",
                description=(
                    "Filter by genre name. Accepts names in English or Polish. Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="platforms",
                description=(
                    "Filter by platform name. Accepts names in English or Polish. Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="game_type",
                description=(
                    "Filter by game type name. Accepts names in English or Polish. Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="game_status",
                description=(
                    "Filter by game status name. Accepts names in English or Polish. "
                    "Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="game_engines",
                description=(
                    "Filter by game engine name. Accepts names in English or Polish. "
                    "Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="game_modes",
                description=(
                    "Filter by game mode name. Accepts names in English or Polish. Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="player_perspectives",
                description=(
                    "Filter by player perspective name. Accepts names in English or Polish. "
                    "Can be specified multiple times."
                ),
            ),
            OpenApiParameter(
                name="external_games",
                description=(
                    "Filter by external game source. Accepts external game source IDs. "
                    "Can be specified multiple times (e.g. to filter games available on Steam or GOG)."
                ),
            ),
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order results by field. "
                    "Accepted values: rank_position, -rank_position, popularity, -popularity, "
                    "release_date, -release_date, created_at, -created_at. "
                    "Prefix with '-' for descending."
                ),
            ),
        ],
    ),
    retrieve=extend_schema(
        description=(
            "Retrieve a single game by ID. "
            "The detail response includes full relations: genres, platforms, publisher, developer, "
            "game engines, game modes, player perspectives, DLCs, expansions, bundles, "
            "and other related game entries."
        ),
    ),
)
class GameViewSet(ReadOnlyModelViewSet[Game]):
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
    ) -> type[GameSerializer | GameSimpleListSerializer]:
        """Get the serializer class for the Game model."""
        if self.action in ("list", "release_calendar"):
            return GameSimpleListSerializer
        return GameSerializer

    @extend_schema(
        description=(
            "Return all games releasing within a specified date range, grouped by day. "
            "Both `start_date` and `end_date` are required; the range must span at most 31 days. "
            "Up to 3 games per day are included in the response, ordered by release date and "
            "then by descending popularity. Returns an empty list if no games fall in the range."
        ),
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


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game genres. "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact genre ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by genre name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the genre's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single genre by ID.",
    ),
)
class GenreViewSet(ReadOnlyModelViewSet[Genre]):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GenreFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all gaming platforms. "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact platform ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by platform name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the platform's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single platform by ID.",
    ),
)
class PlatformViewSet(ReadOnlyModelViewSet[Platform]):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlatformFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game types (e.g. main game, DLC, expansion). "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by type label (bilingual EN/PL) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game type ID.",
            ),
            OpenApiParameter(
                name="type",
                description=(
                    "Filter by game type label. Searches both the English and Polish type fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the game type's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single game type by ID.",
    ),
)
class GameTypeViewSet(ReadOnlyModelViewSet[GameType]):
    """A ViewSet for the GameType model."""

    queryset = GameType.objects.all()
    serializer_class = GameTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameTypeFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game development statuses (e.g. Released, In Development, Cancelled). "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by status label (bilingual EN/PL) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game status ID.",
            ),
            OpenApiParameter(
                name="status",
                description=(
                    "Filter by status label. Searches both the English and Polish status fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the game status's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single game status by ID.",
    ),
)
class GameStatusViewSet(ReadOnlyModelViewSet[GameStatus]):
    """A ViewSet for the GameStatus model."""

    queryset = GameStatus.objects.all()
    serializer_class = GameStatusSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameStatusFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game engines (e.g. Unreal Engine, Unity). "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game engine ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by engine name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the game engine's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single game engine by ID.",
    ),
)
class GameEngineViewSet(ReadOnlyModelViewSet[GameEngine]):
    """A ViewSet for the GameEngine model."""

    queryset = GameEngine.objects.all()
    serializer_class = GameEngineSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameEngineFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game modes (e.g. Single player, Multiplayer, Co-operative). "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game mode ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by game mode name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the game mode's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single game mode by ID.",
    ),
)
class GameModeViewSet(ReadOnlyModelViewSet[GameMode]):
    """A ViewSet for the GameMode model."""

    queryset = GameMode.objects.all()
    serializer_class = GameModeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameModeFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all player perspectives (e.g. First person, Third person, Side view). "
            "This is a read-only Dictionary Model sourced from IGDB. "
            "Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact player perspective ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by perspective name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the player perspective's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single player perspective by ID.",
    ),
)
class PlayerPerspectiveViewSet(ReadOnlyModelViewSet[PlayerPerspective]):
    """A ViewSet for the PlayerPerspective model."""

    queryset = PlayerPerspective.objects.all()
    serializer_class = PlayerPerspectiveSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlayerPerspectiveFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all external game sources (e.g. Steam, GOG, Epic Games Store). "
            "This is a read-only Dictionary Model used to link games to their entries on "
            "external platforms. Filter by name (bilingual EN/PL partial match) or IGDB ID."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact external game source ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by source name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
            OpenApiParameter(
                name="igdb_id",
                description="Filter by the external source's IGDB identifier.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single external game source by ID.",
    ),
)
class ExternalGameSourceViewSet(ReadOnlyModelViewSet[ExternalGameSource]):
    """A ViewSet for the ExternalGameSource model."""

    queryset = ExternalGameSource.objects.all()
    serializer_class = ExternalGameSourceSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = ExternalGameSourceFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List all game media asset types. "
            "This is a Dictionary Model that categorises game media by type (e.g. banner, cover). "
            "Filter by name (bilingual EN/PL partial match)."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact game media ID.",
            ),
            OpenApiParameter(
                name="name",
                description=(
                    "Filter by media type name. Searches both the English and Polish name fields "
                    "(case-insensitive partial match)."
                ),
            ),
        ],
    ),
    create=extend_schema(
        description="Create a new game media record. Requires administrator privileges.",
    ),
    retrieve=extend_schema(
        description="Retrieve a single game media record by ID.",
    ),
    update=extend_schema(
        description="Replace all fields of a game media record. Requires administrator privileges.",
    ),
    partial_update=extend_schema(
        description="Update one or more fields of a game media record. Requires administrator privileges.",
    ),
    destroy=extend_schema(
        description="Delete a game media record. Requires administrator privileges.",
    ),
)
class GameMediaViewSet(ModelViewSet[GameMedia]):
    """A ViewSet for the GameMedia model."""

    queryset = GameMedia.objects.all()
    serializer_class = GameMediaSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameMediaFilterSet
