from ..exceptions import CompressorError as CompressorError
from .base import BaseCompressor as BaseCompressor

class LzmaCompressor(BaseCompressor):
    min_length: int
    preset: int
    def compress(self, value: bytes) -> bytes: ...
    def decompress(self, value: bytes) -> bytes: ...
