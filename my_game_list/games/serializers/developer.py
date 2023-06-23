"""This module contains the serializers for the Developer model."""
from my_game_list.games.models import Developer
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class DeveloperSerializer(BaseDictionarySerializer):
    """A serializer for the developer model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for developer serializer."""

        model = Developer
