from .base import BaseCompressor as BaseCompressor

class IdentityCompressor(BaseCompressor):
    def compress(self, value: bytes) -> bytes: ...
    def decompress(self, value: bytes) -> bytes: ...
