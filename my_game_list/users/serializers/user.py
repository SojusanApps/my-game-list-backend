from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer used during the user registration process."""

    class Meta:
        """Meta data for the class."""

        model = User
        fields = ("username", "password", "email", "avatar")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str):
        """The validation function for password."""
        django_validate_password(value)
        return value

    def create(self, validated_data: dict):
        """Create a new User instance."""
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            avatar=validated_data.get("avatar", b""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
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
