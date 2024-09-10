"""This module contains the serializers for the GameList model."""

from rest_framework import serializers

from my_game_list.games.models import GameList


class GameListSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list model."""

    status = serializers.CharField(source="get_status_display", read_only=True)
    status_code = serializers.CharField(source="status")
    game_id = serializers.IntegerField(source="game.id", read_only=True)
    title = serializers.CharField(source="game.title", read_only=True)
    game_cover_image = serializers.CharField(source="game.cover_image_id", read_only=True)

    class Meta:
        """Meta data for the game list serializer."""

        model = GameList
        fields = (
            "id",
            "status",
            "status_code",
            "score",
            "created_at",
            "last_modified_at",
            "game_id",
            "title",
            "game_cover_image",
            "user",
        )


class GameListCreateSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list create model."""

    class Meta:
        """Meta data for the game list create serializer."""

        model = GameList
        fields = (
            "id",
            "status",
            "score",
            "created_at",
            "last_modified_at",
            "game",
            "user",
        )
