class CacheKey(str):
    def original_key(self) -> str: ...

def default_reverse_key(key: str) -> str: ...
