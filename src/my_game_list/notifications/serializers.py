"""This module contains serializers for the notification system."""

from typing import Any

from django.contrib.auth import get_user_model
from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema_field
from rest_framework import serializers

from my_game_list.notifications.models import Notification

User = get_user_model()


class NotificationGenericActorSerializer(serializers.Serializer[Any]):
    """Serializer for generic notification actors."""

    id = serializers.IntegerField()
    str = serializers.CharField()
    type = serializers.CharField()


class NotificationUserActorSerializer(NotificationGenericActorSerializer):
    """Serializer for user notification actors."""

    gravatar_url = serializers.CharField()


actor_serializer = PolymorphicProxySerializer(
    component_name="NotificationActor",
    # Needs to explicitly specify any supported actor types here for correct OpenAPI schema generation.
    serializers={
        "user": NotificationUserActorSerializer,
    },
    resource_type_field_name="type",
)


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

    @extend_schema_field(actor_serializer)
    def get_actor(self, obj: Notification) -> dict[str, Any] | None:
        """Get the actor representation."""
        if obj.actor:
            data: dict[str, Any] = {"id": obj.actor.pk, "str": str(obj.actor), "type": obj.actor_content_type.model}
            if isinstance(obj.actor, User):
                data["gravatar_url"] = obj.actor.gravatar_url
            return data
        return None

    @extend_schema_field(actor_serializer)
    def get_target(self, obj: Notification) -> dict[str, Any] | None:
        """Get the target representation."""
        if obj.target and obj.target_content_type:
            data: dict[str, Any] = {"id": obj.target.pk, "str": str(obj.target), "type": obj.target_content_type.model}
            if isinstance(obj.target, User):
                data["gravatar_url"] = obj.target.gravatar_url
            return data
        return None
