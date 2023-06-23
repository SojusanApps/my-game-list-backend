"""This module contains the base class for all dictionary serializers."""
from rest_framework import serializers


class BaseDictionarySerializer(serializers.ModelSerializer):
    """A base serializer for dictionary models."""

    class Meta:
        """Meta data for dictionary models."""

        fields = ("id", "name")
