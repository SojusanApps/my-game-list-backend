from _typeshed import Incomplete
from collections.abc import Generator

iswin32: Incomplete
import_errors: Incomplete

class Checkers:
    path: Incomplete
    def __init__(self, path: Incomplete) -> None: ...
    def dir(self) -> None: ...
    def file(self) -> None: ...
    def dotfile(self) -> Incomplete: ...
    def ext(self, arg: Incomplete) -> Incomplete: ...
    def exists(self) -> None: ...
    def basename(self, arg: Incomplete) -> Incomplete: ...
    def basestarts(self, arg: Incomplete) -> Incomplete: ...
    def relto(self, arg: Incomplete) -> Incomplete: ...
    def fnmatch(self, arg: Incomplete) -> Incomplete: ...
    def endswith(self, arg: Incomplete) -> Incomplete: ...

class NeverRaised(Exception): ...

class PathBase:
    Checkers = Checkers
    def __div__(self, other: Incomplete) -> Incomplete: ...
    __truediv__ = __div__
    def basename(self) -> Incomplete: ...
    def dirname(self) -> Incomplete: ...
    def purebasename(self) -> Incomplete: ...
    def ext(self) -> Incomplete: ...
    def dirpath(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def read_binary(self) -> Incomplete: ...
    def read_text(self, encoding: Incomplete) -> Incomplete: ...
    def read(self, mode: str = ...) -> Incomplete: ...
    def readlines(self, cr: int = ...) -> Incomplete: ...
    def load(self) -> Incomplete: ...
    def move(self, target: Incomplete) -> None: ...
    def check(self, **kw: Incomplete) -> Incomplete: ...
    def fnmatch(self, pattern: Incomplete) -> Incomplete: ...
    def relto(self, relpath: Incomplete) -> Incomplete: ...
    def ensure_dir(self, *args: Incomplete) -> Incomplete: ...
    def bestrelpath(self, dest: Incomplete) -> Incomplete: ...
    def exists(self) -> Incomplete: ...
    def isdir(self) -> Incomplete: ...
    def isfile(self) -> Incomplete: ...
    def parts(self, reverse: bool = ...) -> Incomplete: ...
    def common(self, other: Incomplete) -> Incomplete: ...
    def __add__(self, other: Incomplete) -> Incomplete: ...
    def __cmp__(self, other: Incomplete) -> Incomplete: ...
    def __lt__(self, other: Incomplete) -> Incomplete: ...
    def visit(
        self,
        fil: Incomplete | None = ...,
        rec: Incomplete | None = ...,
        ignore: Incomplete = ...,
        bf: bool = ...,
        sort: bool = ...,
    ) -> Generator[Incomplete, None, None]: ...
    def samefile(self, other: Incomplete) -> Incomplete: ...
    def __fspath__(self) -> Incomplete: ...

class Visitor:
    rec: Incomplete
    fil: Incomplete
    ignore: Incomplete
    breadthfirst: Incomplete
    optsort: Incomplete
    def __init__(
        self, fil: Incomplete, rec: Incomplete, ignore: Incomplete, bf: Incomplete, sort: Incomplete
    ) -> None: ...
    def gen(self, path: Incomplete) -> Generator[Incomplete, None, None]: ...

class FNMatcher:
    pattern: Incomplete
    def __init__(self, pattern: Incomplete) -> None: ...
    def __call__(self, path: Incomplete) -> Incomplete: ...