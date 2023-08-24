import py
from _typeshed import Incomplete
from py._path import common as common

class cache:
    proplist: Incomplete
    info: Incomplete
    entries: Incomplete
    prop: Incomplete

class RepoEntry:
    url: Incomplete
    rev: Incomplete
    timestamp: Incomplete
    def __init__(self, url: Incomplete, rev: Incomplete, timestamp: Incomplete) -> None: ...

class RepoCache:
    timeout: int
    repos: Incomplete
    def __init__(self) -> None: ...
    def clear(self) -> None: ...
    def put(self, url: Incomplete, rev: Incomplete, timestamp: Incomplete | None = ...) -> None: ...
    def get(self, url: Incomplete) -> Incomplete: ...

repositories: Incomplete
ALLOWED_CHARS: str
ALLOWED_CHARS_HOST: Incomplete

def checkbadchars(url: Incomplete) -> None: ...

class SvnPathBase(common.PathBase):
    sep: str
    url: Incomplete
    def __hash__(self) -> Incomplete: ...
    def new(self, **kw: Incomplete) -> Incomplete: ...
    def __eq__(self, other: Incomplete) -> Incomplete: ...
    def __ne__(self, other: Incomplete) -> Incomplete: ...
    def join(self, *args: Incomplete) -> Incomplete: ...
    def propget(self, name: Incomplete) -> Incomplete: ...
    def proplist(self) -> Incomplete: ...
    def size(self) -> Incomplete: ...
    def mtime(self) -> Incomplete: ...

    class Checkers(common.Checkers):
        def dir(self) -> Incomplete: ...
        def file(self) -> Incomplete: ...
        def exists(self) -> Incomplete: ...

def parse_apr_time(timestr: Incomplete) -> Incomplete: ...

class PropListDict(dict[Incomplete, Incomplete]):
    path: Incomplete
    def __init__(self, path: Incomplete, keynames: Incomplete) -> None: ...
    def __getitem__(self, key: Incomplete) -> Incomplete: ...

def fixlocale() -> Incomplete: ...

ILLEGAL_CHARS: Incomplete
ISWINDOWS: Incomplete

def path_to_fspath(path: Incomplete, addat: bool = ...) -> Incomplete: ...
def url_from_path(path: Incomplete) -> Incomplete: ...

class SvnAuth:
    username: Incomplete
    password: Incomplete
    cache_auth: Incomplete
    interactive: Incomplete
    def __init__(
        self, username: Incomplete, password: Incomplete, cache_auth: bool = ..., interactive: bool = ...
    ) -> None: ...
    def makecmdoptions(self) -> Incomplete: ...

rex_blame: Incomplete

class SvnWCCommandPath(common.PathBase):
    sep: Incomplete
    localpath: Incomplete
    auth: Incomplete
    def __new__(cls, wcpath: Incomplete | None = ..., auth: Incomplete | None = ...) -> Incomplete: ...
    strpath: Incomplete
    rev: Incomplete
    def __eq__(self, other: Incomplete) -> Incomplete: ...
    url: Incomplete
    def dump(self, obj: Incomplete) -> Incomplete: ...
    def svnurl(self) -> Incomplete: ...
    def switch(self, url: Incomplete) -> None: ...
    def checkout(self, url: Incomplete | None = ..., rev: Incomplete | None = ...) -> None: ...
    def update(self, rev: str = ..., interactive: bool = ...) -> None: ...
    def write(self, content: Incomplete, mode: str = ...) -> None: ...
    def dirpath(self, *args: Incomplete) -> Incomplete: ...
    def ensure(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def mkdir(self, *args: Incomplete) -> Incomplete: ...
    def add(self) -> None: ...
    def remove(self, rec: int = ..., force: int = ...) -> None: ...
    def copy(self, target: Incomplete) -> None: ...
    def rename(self, target: Incomplete) -> None: ...
    def lock(self) -> None: ...
    def unlock(self) -> None: ...
    def cleanup(self) -> None: ...
    def status(self, updates: int = ..., rec: int = ..., externals: int = ...) -> Incomplete: ...
    def diff(self, rev: Incomplete | None = ...) -> Incomplete: ...
    def blame(self) -> Incomplete: ...
    def commit(self, msg: str = ..., rec: int = ...) -> Incomplete: ...
    def propset(self, name: Incomplete, value: Incomplete, *args: Incomplete) -> None: ...
    def propget(self, name: Incomplete) -> Incomplete: ...
    def propdel(self, name: Incomplete) -> Incomplete: ...
    def proplist(self, rec: int = ...) -> Incomplete: ...
    def revert(self, rec: int = ...) -> Incomplete: ...
    def new(self, **kw: Incomplete) -> Incomplete: ...
    def join(self, *args: Incomplete, **kwargs: Incomplete) -> Incomplete: ...
    def info(self, usecache: int = ...) -> Incomplete: ...
    def listdir(self, fil: Incomplete | None = ..., sort: Incomplete | None = ...) -> Incomplete: ...
    def open(self, mode: str = ...) -> Incomplete: ...

    class Checkers(py.path.local.Checkers):  # type: ignore[misc, name-defined]
        svnwcpath: Incomplete
        path: Incomplete
        def __init__(self, path: Incomplete) -> None: ...
        def versioned(self) -> Incomplete: ...

    def log(self, rev_start: Incomplete | None = ..., rev_end: int = ..., verbose: bool = ...) -> Incomplete: ...
    def size(self) -> Incomplete: ...
    def mtime(self) -> Incomplete: ...
    def __hash__(self) -> Incomplete: ...

class WCStatus:
    attrnames: Incomplete
    wcpath: Incomplete
    rev: Incomplete
    modrev: Incomplete
    author: Incomplete
    def __init__(
        self,
        wcpath: Incomplete,
        rev: Incomplete | None = ...,
        modrev: Incomplete | None = ...,
        author: Incomplete | None = ...,
    ) -> None: ...
    def allpath(self, sort: bool = ..., **kw: Incomplete) -> Incomplete: ...
    def fromstring(
        data: Incomplete,
        rootwcpath: Incomplete,
        rev: Incomplete | None = ...,
        modrev: Incomplete | None = ...,
        author: Incomplete | None = ...,
    ) -> Incomplete: ...

class XMLWCStatus(WCStatus):
    def fromstring(
        data: Incomplete,
        rootwcpath: Incomplete,
        rev: Incomplete | None = ...,
        modrev: Incomplete | None = ...,
        author: Incomplete | None = ...,
    ) -> Incomplete: ...

class InfoSvnWCCommand:
    url: Incomplete
    kind: Incomplete
    rev: Incomplete
    path: Incomplete
    size: Incomplete
    created_rev: Incomplete
    last_author: Incomplete
    mtime: Incomplete
    time: Incomplete
    def __init__(self, output: Incomplete) -> None: ...
    def __eq__(self, other: Incomplete) -> Incomplete: ...

def parse_wcinfotime(timestr: Incomplete) -> Incomplete: ...
def make_recursive_propdict(wcroot: Incomplete, output: Incomplete, rex: Incomplete = ...) -> Incomplete: ...
def importxml(cache: Incomplete = ...) -> Incomplete: ...

class LogEntry:
    rev: Incomplete
    author: Incomplete
    msg: Incomplete
    date: Incomplete
    strpaths: Incomplete
    def __init__(self, logentry: Incomplete) -> None: ...