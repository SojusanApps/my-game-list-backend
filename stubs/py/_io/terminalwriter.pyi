import ctypes
from _typeshed import Incomplete
from py._builtin import bytes as bytes, text as text

py3k: Incomplete
py33: Incomplete
win32_and_ctypes: bool
colorama: Incomplete

def get_terminal_width() -> Incomplete: ...

terminal_width: Incomplete
char_width: Incomplete

def get_line_width(text: Incomplete) -> Incomplete: ...
def ansi_print(
    text: Incomplete,
    esc: Incomplete,
    file: Incomplete | None = ...,
    newline: bool = ...,
    flush: bool = ...,
) -> None: ...
def should_do_markup(file: Incomplete) -> Incomplete: ...

class TerminalWriter:
    stringio: Incomplete
    encoding: Incomplete
    hasmarkup: Incomplete
    def __init__(
        self,
        file: Incomplete | None = ...,
        stringio: bool = ...,
        encoding: Incomplete | None = ...,
    ) -> None: ...
    @property
    def fullwidth(self) -> Incomplete: ...
    @property
    def chars_on_current_line(self) -> Incomplete: ...
    @property
    def width_of_current_line(self) -> Incomplete: ...
    def markup(self, text: Incomplete, **kw: Incomplete) -> Incomplete: ...
    def sep(
        self,
        sepchar: Incomplete,
        title: Incomplete | None = ...,
        fullwidth: Incomplete | None = ...,
        **kw: Incomplete,
    ) -> None: ...
    def write(self, msg: Incomplete, **kw: Incomplete) -> None: ...
    def line(self, s: str = ..., **kw: Incomplete) -> None: ...
    def reline(self, line: Incomplete, **kw: Incomplete) -> None: ...

class Win32ConsoleWriter(TerminalWriter):
    def write(self, msg: Incomplete, **kw: Incomplete) -> None: ...

class WriteFile:
    encoding: Incomplete
    def __init__(self, writemethod: Incomplete, encoding: Incomplete | None = ...) -> None: ...
    def write(self, data: Incomplete) -> None: ...
    def flush(self) -> None: ...

STD_OUTPUT_HANDLE: int
STD_ERROR_HANDLE: int
FOREGROUND_BLACK: int
FOREGROUND_BLUE: int
FOREGROUND_GREEN: int
FOREGROUND_RED: int
FOREGROUND_WHITE: int
FOREGROUND_INTENSITY: int
BACKGROUND_BLACK: int
BACKGROUND_BLUE: int
BACKGROUND_GREEN: int
BACKGROUND_RED: int
BACKGROUND_WHITE: int
BACKGROUND_INTENSITY: int
SHORT = ctypes.c_short

class COORD(ctypes.Structure): ...
class SMALL_RECT(ctypes.Structure): ...
class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure): ...

def GetStdHandle(kind: Incomplete) -> Incomplete: ...

SetConsoleTextAttribute: Incomplete

def GetConsoleInfo(handle: Incomplete) -> Incomplete: ...
def write_out(fil: Incomplete, msg: Incomplete) -> None: ...
