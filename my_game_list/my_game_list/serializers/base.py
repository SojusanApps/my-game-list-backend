"""This module contains the base class for all dictionary serializers."""
from typing import Any

from rest_framework import serializers


class BaseDictionarySerializer(serializers.ModelSerializer[Any]):
    """A base serializer for dictionary models."""

    class Meta:
        """Meta data for dictionary models."""

        fields = ("id", "name")
