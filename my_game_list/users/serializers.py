from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer used during the user registration process."""

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "avatar", "gender")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str):
        validate_password(value)
        return value

    def create(self, validated_data: dict):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data["gender"],
            avatar=validated_data["avatar"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ListUserSerializer(serializers.ModelSerializer):
    """Serializer for listing the user model."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "date_joined",
            "avatar",
            "gender",
            "is_active",
        )
        read_only_fields = ("id", "avatar", "last_login", "date_joined")
