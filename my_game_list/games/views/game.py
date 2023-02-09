from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import Game
from my_game_list.games.serializers import GameSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class GameViewSet(ModelViewSet):
    """A ViewSet for the Game model."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAdminOrReadOnly,)
