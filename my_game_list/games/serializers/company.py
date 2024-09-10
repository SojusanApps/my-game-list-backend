"""This module contains the serializers for the Company model."""

from rest_framework import serializers

from my_game_list.games.models import Company
from my_game_list.my_game_list.serializers import BaseDictionarySerializer


class CompanySimpleNameSerializer(serializers.ModelSerializer[Company]):
    """A simple serializer for the Company model."""

    class Meta:
        """Meta data for simple Company serializer."""

        model = Company
        fields = ("id", "name")


class CompanySerializer(BaseDictionarySerializer):
    """A serializer for the Company model."""

    class Meta(BaseDictionarySerializer.Meta):
        """Meta data for Company serializer."""

        model = Company
        fields = (*BaseDictionarySerializer.Meta.fields, "company_logo_id", "igdb_id")
