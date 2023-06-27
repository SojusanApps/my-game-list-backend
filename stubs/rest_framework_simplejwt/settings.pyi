from .utils import format_lazy as format_lazy
from _typeshed import Incomplete
from rest_framework.settings import APISettings as _APISettings

USER_SETTINGS: Incomplete
DEFAULTS: Incomplete
IMPORT_STRINGS: Incomplete
REMOVED_SETTINGS: Incomplete

class APISettings(_APISettings): ...

api_settings: _APISettings

def reload_api_settings(*args: Incomplete, **kwargs: Incomplete) -> None: ...
