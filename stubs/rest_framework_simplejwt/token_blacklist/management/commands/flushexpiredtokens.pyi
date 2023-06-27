from ...models import OutstandingToken as OutstandingToken
from django.core.management.base import BaseCommand
from rest_framework_simplejwt.utils import aware_utcnow as aware_utcnow
from _typeshed import Incomplete

class Command(BaseCommand):
    help: str
    def handle(self, *args: Incomplete, **kwargs: Incomplete) -> None: ...
