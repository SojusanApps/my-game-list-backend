from django.db.backends.sqlite3 import features, base
from django_prometheus.db.common import DatabaseWrapperMixin as DatabaseWrapperMixin

class DatabaseFeatures(features.DatabaseFeatures): ...

class DatabaseWrapper(DatabaseWrapperMixin, base.DatabaseWrapper):
    CURSOR_CLASS = base.SQLiteCursorWrapper
