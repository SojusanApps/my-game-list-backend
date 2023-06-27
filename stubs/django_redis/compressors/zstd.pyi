from ..exceptions import CompressorError as CompressorError
from .base import BaseCompressor as BaseCompressor

class ZStdCompressor(BaseCompressor):
    min_length: int
    def compress(self, value: bytes) -> bytes: ...
    def decompress(self, value: bytes) -> bytes: ...
