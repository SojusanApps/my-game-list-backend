"""This module contains the serializers for the Game model."""

from rest_framework import serializers

from my_game_list.games.models import Developer, Game, Genre, Platform, Publisher
from my_game_list.games.serializers.developer import DeveloperSerializer
from my_game_list.games.serializers.genre import GenreSerializer
from my_game_list.games.serializers.platform import PlatformSerializer
from my_game_list.games.serializers.publisher import PublisherSerializer


class GameSerializer(serializers.ModelSerializer[Game]):
    """A serializer for the game model."""

    publisher = PublisherSerializer()
    developer = DeveloperSerializer()
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)

    class Meta:
        """Meta data for game serializer."""

        model = Game
        fields = (
            "id",
            "title",
            "created_at",
            "last_modified_at",
            "release_date",
            "cover_image",
            "description",
            "publisher",
            "developer",
            "genres",
            "platforms",
            "average_score",
            "scores_count",
            "rank_position",
            "members_count",
            "popularity",
        )


class GameCreateSerializer(serializers.ModelSerializer[Game]):
    """A serializer for creating a game item."""

    publisher = serializers.SlugRelatedField(
        queryset=Publisher.objects.all(),
        slug_field="id",
    )
    developer = serializers.SlugRelatedField(
        queryset=Developer.objects.all(),
        slug_field="id",
    )
    genres = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="id",
        many=True,
    )
    platforms = serializers.SlugRelatedField(
        queryset=Platform.objects.all(),
        slug_field="id",
        many=True,
    )

    class Meta:
        """Meta data for game create serializer."""

        model = Game
        fields = (
            "id",
            "title",
            "created_at",
            "last_modified_at",
            "release_date",
            "cover_image",
            "description",
            "publisher",
            "developer",
            "genres",
            "platforms",
        )
