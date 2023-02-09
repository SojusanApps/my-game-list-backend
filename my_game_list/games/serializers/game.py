from rest_framework import serializers

from my_game_list.games.models import Game
from my_game_list.games.serializers.developer import DeveloperSerializer
from my_game_list.games.serializers.genre import GenreSerializer
from my_game_list.games.serializers.platform import PlatformSerializer
from my_game_list.games.serializers.publisher import PublisherSerializer


class GameSerializer(serializers.ModelSerializer):
    """A serializer for the game model."""

    publisher = PublisherSerializer()
    developer = DeveloperSerializer()
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)

    class Meta:
        model = Game
        fields = (
            "id",
            "title",
            "creation_time",
            "last_modified",
            "release_date",
            "cover_image",
            "description",
            "publisher",
            "developer",
            "genres",
            "platforms",
        )
