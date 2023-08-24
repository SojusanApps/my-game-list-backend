from .base import BaseSerializer as BaseSerializer
from typing import Any

class MSGPackSerializer(BaseSerializer):
    def dumps(self, value: Any) -> bytes: ...
    def loads(self, value: bytes) -> Any: ...