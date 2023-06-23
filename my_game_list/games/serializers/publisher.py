"""This module contains the serializers for the Publisher model."""
from my_game_list.games.models import Publisher
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class PublisherSerializer(BaseDictionarySerializer):
    """A serializer for publisher model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for publisher serializer."""

        model = Publisher
