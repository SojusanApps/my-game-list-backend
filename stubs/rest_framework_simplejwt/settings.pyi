from typing import Any

from rest_framework.settings import APISettings as _APISettings

from .utils import format_lazy as format_lazy

USER_SETTINGS: dict[str, Any]
DEFAULTS: dict[str, Any]
IMPORT_STRINGS: tuple[str, ...]
REMOVED_SETTINGS: tuple[str, ...]

class APISettings(_APISettings): ...

api_settings: APISettings

def reload_api_settings(*args: Any, **kwargs: Any) -> None: ...
