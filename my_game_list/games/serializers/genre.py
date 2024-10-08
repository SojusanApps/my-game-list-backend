"""This module contains the serializers for the Genre model."""

from my_game_list.games.models import Genre
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class GenreSerializer(BaseDictionarySerializer):
    """A serializer for genre model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for a genre serializer."""

        model = Genre
        fields = (*BaseDictionarySerializer.Meta.fields, "igdb_id")
