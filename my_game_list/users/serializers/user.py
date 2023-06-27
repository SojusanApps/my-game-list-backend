"""This model contains the serializers for User model."""
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Self

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers

if TYPE_CHECKING:
    from my_game_list.users.models import User as UserType

User: type["UserType"] = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer["UserType"]):
    """Serializer used during the user registration process."""

    class Meta:
        """Meta data for the class."""

        model = User
        fields = ("username", "password", "email", "avatar")
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
            avatar=validated_data.get("avatar", b""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer["UserType"]):
    """Serializer for listing the user model."""

    class Meta:
        """Meta data for the class."""

        model = User
        fields = (
            "id",
            "username",
            "email",
            "last_login",
            "date_joined",
            "avatar",
            "is_active",
        )
        read_only_fields = ("id", "avatar", "last_login", "date_joined")
