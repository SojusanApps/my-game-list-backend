from _typeshed import Incomplete
from django_prometheus.cache.metrics import (
    django_cache_get_fail_total as django_cache_get_fail_total,
    django_cache_get_total as django_cache_get_total,
    django_cache_hits_total as django_cache_hits_total,
    django_cache_misses_total as django_cache_misses_total,
)
from django_redis import cache

class RedisCache(cache.RedisCache):
    def get(
        self,
        key: Incomplete,
        default: Incomplete | None = ...,
        version: Incomplete | None = ...,
        client: Incomplete | None = ...,
    ) -> Incomplete: ...
