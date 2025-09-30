from _typeshed import Incomplete
from py import _path as path, _process as process
from py._path import common as common, svnwc as svncommon
from py._path.cacheutil import (
    AgingCache as AgingCache,
    BuildcostAccessCache as BuildcostAccessCache,
)

DEBUG: bool

class SvnCommandPath(svncommon.SvnPathBase):
    strpath: Incomplete
    rev: Incomplete
    auth: Incomplete
    def __new__(
        cls,
        path: Incomplete,
        rev: Incomplete | None = ...,
        auth: Incomplete | None = ...,
    ) -> Incomplete: ...
    def open(self, mode: str = ...) -> Incomplete: ...
    def dirpath(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def mkdir(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def copy(self, target: Incomplete, msg: str = ...) -> None: ...
    def rename(self, target: Incomplete, msg: str = ...) -> None: ...
    def remove(self, rec: int = ..., msg: str = ...) -> None: ...
    def export(self, topath: Incomplete) -> Incomplete: ...
    def ensure(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def info(self) -> Incomplete: ...
    def listdir(self, fil: Incomplete | None = ..., sort: Incomplete | None = ...) -> Incomplete: ...
    def log(
        self,
        rev_start: Incomplete | None = ...,
        rev_end: int = ...,
        verbose: bool = ...,
    ) -> Incomplete: ...

class InfoSvnCommand:
    lspattern: Incomplete
    kind: str
    created_rev: Incomplete
    last_author: Incomplete
    size: Incomplete
    mtime: Incomplete
    time: Incomplete
    def __init__(self, line: Incomplete) -> None: ...
    def __eq__(self, other: Incomplete) -> Incomplete: ...

def parse_time_with_missing_year(timestr: Incomplete) -> Incomplete: ...

class PathEntry:
    strpath: Incomplete
    action: Incomplete
    copyfrom_path: Incomplete
    copyfrom_rev: Incomplete
    def __init__(self, ppart: Incomplete) -> None: ...
