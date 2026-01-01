"""This module contains the viewsets for the game related data."""

from typing import TYPE_CHECKING, Self

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

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
)
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly

if TYPE_CHECKING:
    from django.db.models import QuerySet


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
    ordering_fields = ("release_date", "created_at")
    ordering = ("release_date",)

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
        if self.action == "list":
            return GameSimpleListSerializer
        return GameSerializer


class GenreViewSet(ModelViewSet[Genre]):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GenreFilterSet


class PlatformViewSet(ModelViewSet[Platform]):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlatformFilterSet


class GameTypeViewSet(ModelViewSet[GameType]):
    """A ViewSet for the GameType model."""

    queryset = GameType.objects.all()
    serializer_class = GameTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameTypeFilterSet


class GameStatusViewSet(ModelViewSet[GameStatus]):
    """A ViewSet for the GameStatus model."""

    queryset = GameStatus.objects.all()
    serializer_class = GameStatusSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameStatusFilterSet


class GameEngineViewSet(ModelViewSet[GameEngine]):
    """A ViewSet for the GameEngine model."""

    queryset = GameEngine.objects.all()
    serializer_class = GameEngineSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameEngineFilterSet


class GameModeViewSet(ModelViewSet[GameMode]):
    """A ViewSet for the GameMode model."""

    queryset = GameMode.objects.all()
    serializer_class = GameModeSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameModeFilterSet


class PlayerPerspectiveViewSet(ModelViewSet[PlayerPerspective]):
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
