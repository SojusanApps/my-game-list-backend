"""This model contains the serializers for User model."""

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from my_game_list.games.models import GameListStatus

if TYPE_CHECKING:
    from my_game_list.users.models import User as UserType

User: type["UserType"] = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer["UserType"]):
    """Serializer used during the user registration process."""

    class Meta:
        """Meta data for the class."""

        model = User
        fields = ("username", "password", "email", "gender")
        extra_kwargs: ClassVar[dict[str, dict[str, bool]]] = {"password": {"write_only": True}}

    def validate_password(self: Self, value: str) -> str:
        """The validation function for password."""
        django_validate_password(value)
        return value

    def create(self: Self, validated_data: Mapping[str, Any]) -> "UserType":
        """Create a new User instance."""
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSimpleSerializer(serializers.ModelSerializer["UserType"]):
    """Simple user serializer with only avatar and url to the details."""

    class Meta:
        """Meta data for the class."""

        model = User
        fields = ("id", "gravatar_url")


class UserSerializer(serializers.ModelSerializer["UserType"]):
    """Serializer for listing the user model."""

    gender = serializers.CharField(source="get_gender_display", read_only=True)

    class Meta:
        """Meta data for the class."""

        model = User
        fields = (
            "id",
            "username",
            "email",
            "gender",
            "last_login",
            "date_joined",
            "gravatar_url",
            "is_active",
        )
        read_only_fields = ("id", "gravatar_url", "last_login", "date_joined")


class UserDetailSerializer(serializers.ModelSerializer["UserType"]):
    """Detailed serializer for User model."""

    gender = serializers.CharField(source="get_gender_display", read_only=True)
    game_list_statistics = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()
    latest_game_list_updates = serializers.SerializerMethodField()

    class Meta:
        """Meta data for the class."""

        model = User
        fields = (
            "id",
            "username",
            "gender",
            "last_login",
            "date_joined",
            "gravatar_url",
            "game_list_statistics",
            "friends",
            "latest_game_list_updates",
        )

    def get_game_list_statistics(self: Self, instance: "UserType") -> dict[str, int]:
        """Get the game list statistics for the user."""
        return {
            "completed": instance.game_lists.filter(status=GameListStatus.COMPLETED).count(),
            "dropped": instance.game_lists.filter(status=GameListStatus.DROPPED).count(),
            "plan_to_play": instance.game_lists.filter(status=GameListStatus.PLAN_TO_PLAY).count(),
            "on_hold": instance.game_lists.filter(status=GameListStatus.ON_HOLD).count(),
            "playing": instance.game_lists.filter(status=GameListStatus.PLAYING).count(),
            "total": instance.game_lists.count(),
            "mean_score": instance.game_lists.aggregate(mean_score=Avg("score"))["mean_score"],
        }

    def get_friends(self: Self, instance: "UserType") -> ReturnDict[Any, Any]:
        """Get the list of friends for the user."""
        friendships = instance.friends.all()[:5]
        friends = [friendship.friend for friendship in friendships]
        return UserSimpleSerializer(friends, many=True, context=self.context).data

    def get_latest_game_list_updates(self: Self, instance: "UserType") -> ReturnDict[Any, Any]:
        """Get the latest game list updates for the user."""
        from my_game_list.games.serializers.game_list import GameListSerializer

        return GameListSerializer(
            instance.game_lists.all().order_by("last_modified_at")[:5],
            many=True,
            context=self.context,
        ).data
