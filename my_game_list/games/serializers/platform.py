"""This module contains the serializers for the Platform model."""

from my_game_list.games.models import Platform
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class PlatformSerializer(BaseDictionarySerializer):
    """A serializer for the platform model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for the platform serializer."""

        model = Platform
