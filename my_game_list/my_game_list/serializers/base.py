from rest_framework import serializers


class BaseDictionarySerializer(serializers.ModelSerializer):
    """A base serializer for dictionary models."""

    class Meta:
        fields = ("id", "name")
