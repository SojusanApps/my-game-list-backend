from .base import BaseSerializer as BaseSerializer
from django.core.serializers.json import DjangoJSONEncoder
from typing import Any

class JSONSerializer(BaseSerializer):
    encoder_class = DjangoJSONEncoder
    def dumps(self, value: Any) -> bytes: ...
    def loads(self, value: bytes) -> Any: ...
