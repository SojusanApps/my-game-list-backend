"""This module contains the serializers for the Publisher model."""

from rest_framework import serializers

from my_game_list.games.models import Publisher
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class PublisherSimpleNameSerializer(serializers.ModelSerializer[Publisher]):
    """A simple serializer for the Publisher model."""

    class Meta:
        """Meta data for simple publisher serializer."""

        model = Publisher
        fields = ("id", "name")


class PublisherSerializer(BaseDictionarySerializer):
    """A serializer for publisher model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for publisher serializer."""

        model = Publisher
        fields = (*BaseDictionarySerializer.Meta.fields, "publisher_logo")
