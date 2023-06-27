from _typeshed import Incomplete
from django.db.backends.mysql import base, features
from django_prometheus.db.common import (
    DatabaseWrapperMixin as DatabaseWrapperMixin,
    ExportingCursorWrapper as ExportingCursorWrapper,
)

class DatabaseFeatures(features.DatabaseFeatures): ...

class DatabaseWrapper(DatabaseWrapperMixin, base.DatabaseWrapper):
    CURSOR_CLASS = base.CursorWrapper
    def create_cursor(self, name: Incomplete | None = ...) -> Incomplete: ...
