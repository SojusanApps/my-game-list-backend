from my_game_list.games.models import Genre
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class GenreSerializer(BaseDictionarySerializer):
    """A serializer for genre model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Genre
