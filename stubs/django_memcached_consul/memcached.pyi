from django.core.cache.backends import memcached
from _typeshed import Incomplete

def get_servers(params: Incomplete) -> Incomplete: ...
def get_servers_list_from_consul(params: Incomplete) -> Incomplete: ...

class BaseMemcachedCache(memcached.BaseMemcachedCache):
    def __init__(
        self, server: Incomplete, params: Incomplete, library: Incomplete, value_not_found_exception: Incomplete
    ) -> None: ...

class MemcachedCache(BaseMemcachedCache):
    def __init__(self, server: Incomplete, params: Incomplete) -> None: ...
