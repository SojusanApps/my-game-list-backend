from .default import DefaultClient as DefaultClient
from _typeshed import Incomplete

def replace_query(url: Incomplete, query: Incomplete) -> Incomplete: ...

class SentinelClient(DefaultClient):
    def __init__(self, server: Incomplete, params: Incomplete, backend: Incomplete) -> None: ...
    def connect(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
