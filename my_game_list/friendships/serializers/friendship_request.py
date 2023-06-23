"""This module contains the serializers for the FriendshipRequest model."""
from collections.abc import Mapping
from typing import Any

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SlugRelatedField, ValidationError

from my_game_list.friendships.models import FriendshipRequest
from my_game_list.users.serializers import UserSerializer

User = get_user_model()


class FriendshipRequestSerializer(ModelSerializer):
    """Serializer for listing the friendship requests."""

    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        """Meta data for the friendship request serializer."""

        model = FriendshipRequest
        fields = (
            "id",
            "rejected_at",
            "created_at",
            "last_modified_at",
            "message",
            "sender",
            "receiver",
        )
        read_only_fields = ("id", "created_at")


class FriendshipRequestCreateSerializer(ModelSerializer):
    """A serializer for creating a friendship request."""

    sender = SlugRelatedField(queryset=User.objects.all(), slug_field="id")
    receiver = SlugRelatedField(queryset=User.objects.all(), slug_field="id")

    class Meta(FriendshipRequestSerializer.Meta):
        """Meta data for the friendship request create serializer."""

        model = FriendshipRequest
        fields = ("message", "sender", "receiver")

    def validate(self, data: Mapping[str, Any]) -> dict[str, Any]:
        """Validate the data passed in the request."""
        sender = data["sender"]
        receiver = data["receiver"]
        if sender == receiver:
            raise ValidationError(_("Can't create friendship request to yourself."))

        if sender.friends.are_friends(sender, receiver):
            raise ValidationError(_("You are already friends."))

        if sender.friends.request_is_sent(sender, receiver):
            raise ValidationError(_("You already sent a friendship request to this user."))

        if sender.friends.request_is_sent(receiver, sender):
            raise ValidationError(_("This user already sent a friendship request to you."))

        return data
