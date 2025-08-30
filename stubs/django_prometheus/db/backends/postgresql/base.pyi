from _typeshed import Incomplete
from django.db.backends.postgresql import base
from django_prometheus.db.backends.common import (
    get_postgres_cursor_class as get_postgres_cursor_class,
)
from django_prometheus.db.common import (
    DatabaseWrapperMixin as DatabaseWrapperMixin,
    ExportingCursorWrapper as ExportingCursorWrapper,
)

class DatabaseWrapper(DatabaseWrapperMixin, base.DatabaseWrapper):
    def get_new_connection(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def create_cursor(self, name: Incomplete | None = ...) -> Incomplete: ...
