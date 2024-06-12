"""This module contains the serializers for the Developer model."""
from rest_framework import serializers

from my_game_list.games.models import Developer
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class DeveloperSimpleNameSerializer(serializers.ModelSerializer[Developer]):
    """A simple serializer for the Developer model."""

    class Meta:
        """Meta data for simple developer serializer."""

        model = Developer
        fields = ("id", "name")


class DeveloperSerializer(BaseDictionarySerializer):
    """A serializer for the developer model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for developer serializer."""

        model = Developer
        fields = (*BaseDictionarySerializer.Meta.fields, "developer_logo")
