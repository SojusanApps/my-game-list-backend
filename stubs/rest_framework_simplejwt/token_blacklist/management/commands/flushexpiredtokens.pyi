from typing import Any

from django.core.management.base import BaseCommand

from ...models import OutstandingToken as OutstandingToken
from ...utils import aware_utcnow as aware_utcnow

class Command(BaseCommand):
    help: str

    def handle(self, *args: Any, **kwargs: Any) -> None: ...
