from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import (
    Developer,
    Game,
    GameFollow,
    GameList,
    GameReview,
    Genre,
    Platform,
    Publisher,
)
from my_game_list.games.serializers import (
    DeveloperSerializer,
    GameFollowSerializer,
    GameListSerializer,
    GameReviewSerializer,
    GameSerializer,
    GenreSerializer,
    PlatformSerializer,
    PublisherSerializer,
)
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class PublisherViewSet(ModelViewSet):
    """A ViewSet for the Publisher model."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)


class DeveloperViewSet(ModelViewSet):
    """A ViewSet for the Developer model."""

    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ModelViewSet):
    """A ViewSet for the Genre model."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PlatformViewSet(ModelViewSet):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GameViewSet(ModelViewSet):
    """A ViewSet for the Game model."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GameListViewSet(ModelViewSet):
    """A ViewSet for the GameList model."""

    queryset = GameList.objects.all()
    serializer_class = GameListSerializer
    permission_classes = (IsAuthenticated,)


class GameFollowViewSet(ModelViewSet):
    """A ViewSet for the GameFollow model."""

    queryset = GameFollow.objects.all()
    serializer_class = GameFollowSerializer
    permission_classes = (IsAuthenticated,)


class GameReviewViewSet(ModelViewSet):
    """A ViewSet for the GameReview model."""

    queryset = GameReview.objects.all()
    serializer_class = GameReviewSerializer
    permission_classes = (IsAuthenticated,)
