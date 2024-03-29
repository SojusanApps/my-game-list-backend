from _typeshed import Incomplete

class Message:
    keywords: Incomplete
    args: Incomplete
    def __init__(self, keywords: Incomplete, args: Incomplete) -> None: ...
    def content(self) -> Incomplete: ...
    def prefix(self) -> Incomplete: ...

class Producer:
    Message = Message
    keywords2consumer: Incomplete
    def __init__(self, keywords: Incomplete, keywordmapper: Incomplete | None = ..., **kw: Incomplete) -> None: ...
    def __getattr__(self, name: Incomplete) -> Incomplete: ...
    def __call__(self, *args: Incomplete) -> None: ...

class KeywordMapper:
    keywords2consumer: Incomplete
    def __init__(self) -> None: ...
    def getstate(self) -> Incomplete: ...
    def setstate(self, state: Incomplete) -> None: ...
    def getconsumer(self, keywords: Incomplete) -> Incomplete: ...
    def setconsumer(self, keywords: Incomplete, consumer: Incomplete) -> None: ...

def default_consumer(msg: Incomplete) -> None: ...

default_keywordmapper: Incomplete

def setconsumer(keywords: Incomplete, consumer: Incomplete) -> None: ...
def setstate(state: Incomplete) -> None: ...
def getstate() -> Incomplete: ...

class File:
    def __init__(self, f: Incomplete) -> None: ...
    def __call__(self, msg: Incomplete) -> None: ...

class Path:
    def __init__(
        self, filename: Incomplete, append: bool = ..., delayed_create: bool = ..., buffering: bool = ...
    ) -> None: ...
    def __call__(self, msg: Incomplete) -> None: ...

def STDOUT(msg: Incomplete) -> None: ...
def STDERR(msg: Incomplete) -> None: ...

class Syslog:
    priority: Incomplete
    def __init__(self, priority: Incomplete | None = ...) -> None: ...
    def __call__(self, msg: Incomplete) -> None: ...
