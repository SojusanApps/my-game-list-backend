from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import Game
from my_game_list.games.serializers import GameCreateSerializer, GameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class GameViewSet(ModelViewSet):
    """A ViewSet for the Game model."""

    queryset = Game.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        return GameCreateSerializer if self.action in ["create", "update", "partial_update"] else GameSerializer
