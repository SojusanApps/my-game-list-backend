from my_game_list.games.models import Publisher
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class PublisherSerializer(BaseDictionarySerializer):
    """A serializer for publisher model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Publisher
