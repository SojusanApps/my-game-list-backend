"""This module contains the serializers for the game related data."""

from typing import Self

from rest_framework import serializers

from my_game_list.games.models import (
    Company,
    Game,
    GameFollow,
    GameList,
    GameMedia,
    GameReview,
    Genre,
    Platform,
)
from my_game_list.my_game_list.serializers import BaseDictionarySerializer
from my_game_list.users.models import User
from my_game_list.users.serializers import UserSerializer


class CompanySimpleNameSerializer(serializers.ModelSerializer[Company]):
    """A simple serializer for the Company model."""

    class Meta:
        """Meta data for simple Company serializer."""

        model = Company
        fields = ("id", "name")


class CompanySerializer(BaseDictionarySerializer):
    """A serializer for the Company model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for Company serializer."""

        model = Company
        fields = (*BaseDictionarySerializer.Meta.fields, "company_logo_id", "igdb_id", "igdb_updated_at")


class GameFollowSerializer(serializers.ModelSerializer[GameFollow]):
    """A serializer for the game follow model."""

    class Meta:
        """Meta data for game follow serializer."""

        model = GameFollow
        fields = ("id", "created_at", "game", "user")


class GameMediaSerializer(serializers.ModelSerializer[GameMedia]):
    """A serializer for the game media model."""

    class Meta:
        """Meta data for the game media serializer."""

        model = GameMedia
        fields = ("id", "name")


class GameListSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list model."""

    status = serializers.CharField(source="get_status_display", read_only=True)
    status_code = serializers.CharField(source="status")
    game_id = serializers.IntegerField(source="game.id", read_only=True)
    title = serializers.CharField(source="game.title", read_only=True)
    game_cover_image = serializers.CharField(source="game.cover_image_id", read_only=True)
    owned_on = GameMediaSerializer(many=True)

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
            "owned_on",
        )


class GameListCreateSerializer(serializers.ModelSerializer[GameList]):
    """A serializer for the game list create model."""

    owned_on = serializers.SlugRelatedField(
        queryset=GameMedia.objects.all(),
        slug_field="id",
        many=True,
    )

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
            "owned_on",
        )


class GameReviewSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for the game review model."""

    user = UserSerializer()
    score = serializers.SerializerMethodField()

    class Meta:
        """Meta data for the game review serializer."""

        model = GameReview
        fields = ("id", "score", "created_at", "review", "game", "user")

    def get_score(self: Self, instance: GameReview) -> int | None:
        """Get user score for the this game."""
        game_list_instance = instance.user.game_lists.filter(game__id=instance.game.id).first()
        if game_list_instance:
            return game_list_instance.score
        return None


class GameReviewCreateSerializer(serializers.ModelSerializer[GameReview]):
    """A serializer for creating the game review model."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="id",
    )

    class Meta:
        """Meta data for the game review create serializer."""

        model = GameReview
        fields = ("id", "created_at", "review", "game", "user")


class GenreSerializer(BaseDictionarySerializer):
    """A serializer for genre model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for a genre serializer."""

        model = Genre
        fields = (*BaseDictionarySerializer.Meta.fields, "igdb_id", "igdb_updated_at")


class PlatformSerializer(BaseDictionarySerializer):
    """A serializer for the platform model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for the platform serializer."""

        model = Platform
        fields = (*BaseDictionarySerializer.Meta.fields, "abbreviation", "igdb_id", "igdb_updated_at")


class GameSerializer(serializers.ModelSerializer[Game]):
    """A serializer for the game model."""

    publisher = CompanySerializer()
    developer = CompanySerializer()
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
            "cover_image_id",
            "summary",
            "publisher",
            "igdb_id",
            "igdb_updated_at",
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
        queryset=Company.objects.all(),
        slug_field="id",
    )
    developer = serializers.SlugRelatedField(
        queryset=Company.objects.all(),
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
            "cover_image_id",
            "igdb_id",
            "igdb_updated_at",
            "summary",
            "publisher",
            "developer",
            "genres",
            "platforms",
        )
