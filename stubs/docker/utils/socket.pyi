from ..transport import NpipeSocket as NpipeSocket
from _typeshed import Incomplete
from collections.abc import Generator

STDOUT: int
STDERR: int

class SocketError(Exception): ...

NPIPE_ENDED: int

def read(socket: Incomplete, n: int = ...) -> Incomplete: ...
def read_exactly(socket: Incomplete, n: Incomplete) -> Incomplete: ...
def next_frame_header(socket: Incomplete) -> Incomplete: ...
def frames_iter(socket: Incomplete, tty: Incomplete) -> Incomplete: ...
def frames_iter_no_tty(socket: Incomplete) -> Generator[Incomplete, None, None]: ...
def frames_iter_tty(socket: Incomplete) -> Generator[Incomplete, None, None]: ...
def consume_socket_output(frames: Incomplete, demux: bool = ...) -> Incomplete: ...
def demux_adaptor(stream_id: Incomplete, data: Incomplete) -> Incomplete: ...
