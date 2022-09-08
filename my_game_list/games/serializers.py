from rest_framework import serializers

from my_game_list.games.models import (
    Developer,
    Game,
    GameFollow,
    GameList,
    GameReview,
    Genre,
    Platform,
    Publisher,
)


class BaseDictionarySerializer(serializers.ModelSerializer):
    """A base serializer for dictionary models."""

    class Meta:
        fields = ("id", "name")


class PublisherSerializer(BaseDictionarySerializer):
    """A serializer for publisher model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Publisher


class DeveloperSerializer(BaseDictionarySerializer):
    """A serializer for the developer model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Developer


class GenreSerializer(BaseDictionarySerializer):
    """A serializer for genre model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Genre


class PlatformSerializer(BaseDictionarySerializer):
    """A serializer for the platform model."""

    class Meta(BaseDictionarySerializer.Meta):
        model = Platform


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


class GameListSerializer(serializers.ModelSerializer):
    """A serializer for the game list model."""

    class Meta:
        model = GameList
        fields = ("id", "status", "creation_time", "last_modified", "game", "user")


class GameFollowSerializer(serializers.ModelSerializer):
    """A serializer for the game follow model."""

    class Meta:
        model = GameFollow
        fields = ("id", "creation_time", "game", "user")


class GameReviewSerializer(serializers.ModelSerializer):
    """A serializer for the game review model."""

    class Meta:
        model = GameReview
        fields = ("id", "score", "creation_time", "review", "game", "user")
