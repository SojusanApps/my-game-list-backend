from _typeshed import Incomplete
from django_prometheus.db import (
    connection_errors_total as connection_errors_total,
    connections_total as connections_total,
    errors_total as errors_total,
    execute_many_total as execute_many_total,
    execute_total as execute_total,
    query_duration_seconds as query_duration_seconds,
)

class ExceptionCounterByType:
    def __init__(
        self,
        counter: Incomplete,
        type_label: str = ...,
        extra_labels: Incomplete | None = ...,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, typ: Incomplete, value: Incomplete, traceback: Incomplete) -> None: ...

class DatabaseWrapperMixin:
    def get_new_connection(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def create_cursor(self, name: Incomplete | None = ...) -> Incomplete: ...

def ExportingCursorWrapper(cursor_class: Incomplete, alias: Incomplete, vendor: Incomplete) -> Incomplete: ...
