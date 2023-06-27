from _typeshed import Incomplete
from django_memcached_consul import memcached
from django_prometheus.cache.metrics import (
    django_cache_get_total as django_cache_get_total,
    django_cache_hits_total as django_cache_hits_total,
    django_cache_misses_total as django_cache_misses_total,
)

class MemcachedCache(memcached.MemcachedCache):
    def get(
        self, key: Incomplete, default: Incomplete | None = ..., version: Incomplete | None = ...
    ) -> Incomplete: ...
