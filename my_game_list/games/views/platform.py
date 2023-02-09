from rest_framework.viewsets import ModelViewSet

from my_game_list.games.models import Platform
from my_game_list.games.serializers import PlatformSerializer
from my_game_list.my_game_list.permissions import IsAdminOrReadOnly


class PlatformViewSet(ModelViewSet):
    """A ViewSet for the Platform model."""

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)
