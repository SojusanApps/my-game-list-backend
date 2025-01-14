"""This module contains the viewsets for the game related data."""

from typing import Self

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.filters import (
    CompanyFilterSet,
    GameFilterSet,
    GameFollowFilterSet,
    GameListFilterSet,
    GameMediaFilterSet,
    GameReviewFilterSet,
    GenreFilterSet,
    PlatformFilterSet,
)
from my_game_list.games.mixins import DictionaryAllValuesMixin
from my_game_list.games.models import Company, Game, GameFollow, GameList, GameMedia, GameReview, Genre, Platform
from my_game_list.games.serializers import (
    CompanySerializer,
    CompanySimpleNameSerializer,
    GameCreateSerializer,
    GameFollowSerializer,
    GameListCreateSerializer,
    GameListSerializer,
    GameMediaSerializer,
    GameReviewCreateSerializer,
    GameReviewSerializer,
    GameSerializer,
    GenreSerializer,
    PlatformSerializer,
)
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class CompanyViewSet(ModelViewSet[Company]):
    """A ViewSet for the Company model."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = CompanyFilterSet

    @action(detail=False, methods=("get",), url_path="all-values")
    def all_values(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Return all values of the Company model."""
        data = Company.objects.all().order_by("name")
        serializer = CompanySimpleNameSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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

    def get_serializer_class(self: Self) -> type[GameListCreateSerializer] | type[GameListSerializer]:
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

    def get_serializer_class(self: Self) -> type[GameReviewCreateSerializer] | type[GameReviewSerializer]:
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

    queryset = Game.objects.all().prefetch_related("game_lists").with_rank_position().with_popularity()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameFilterSet
    ordering_fields = ("release_date",)
    ordering = ("release_date",)

    def get_serializer_class(self: Self) -> type[GameCreateSerializer] | type[GameSerializer]:
        """Get the serializer class for the Game model."""
        return GameCreateSerializer if self.action in ["create", "update", "partial_update"] else GameSerializer


class GenreViewSet(ModelViewSet[Genre], DictionaryAllValuesMixin):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GenreFilterSet


class PlatformViewSet(ModelViewSet[Platform], DictionaryAllValuesMixin):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PlatformFilterSet


class GameMediaViewSet(ModelViewSet[GameMedia], DictionaryAllValuesMixin):
    """A ViewSet for the GameMedia model."""

    queryset = GameMedia.objects.all()
    serializer_class = GameMediaSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GameMediaFilterSet
