"""This module contains serializers for the notification system."""

from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_game_list.notifications.models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer[Notification]):
    """Serializer for the Notification model."""

    actor = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        """Meta data for the NotificationSerializer."""

        model = Notification
        fields = (
            "id",
            "level",
            "unread",
            "actor",
            "verb",
            "target",
            "timestamp",
            "description",
            "data",
        )

    def get_actor(self, obj: Notification) -> dict[str, Any] | None:
        """Get the actor representation."""
        if obj.actor:
            data: dict[str, Any] = {"id": obj.actor.pk, "str": str(obj.actor), "type": obj.actor_content_type.model}
            if isinstance(obj.actor, User):
                data["gravatar_url"] = obj.actor.gravatar_url
            return data
        return None

    def get_target(self, obj: Notification) -> dict[str, Any] | None:
        """Get the target representation."""
        if obj.target and obj.target_content_type:
            data: dict[str, Any] = {"id": obj.target.pk, "str": str(obj.target), "type": obj.target_content_type.model}
            if isinstance(obj.target, User):
                data["gravatar_url"] = obj.target.gravatar_url
            return data
        return None
