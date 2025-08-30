from _typeshed import Incomplete
from django.core.cache.backends import filebased
from django_prometheus.cache.metrics import (
    django_cache_get_total as django_cache_get_total,
    django_cache_hits_total as django_cache_hits_total,
    django_cache_misses_total as django_cache_misses_total,
)

class FileBasedCache(filebased.FileBasedCache):
    def get(
        self,
        key: Incomplete,
        default: Incomplete | None = ...,
        version: Incomplete | None = ...,
    ) -> Incomplete: ...
