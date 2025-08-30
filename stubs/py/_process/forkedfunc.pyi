from _typeshed import Incomplete

def get_unbuffered_io(fd: Incomplete, filename: Incomplete) -> Incomplete: ...

class ForkedFunc:
    EXITSTATUS_EXCEPTION: int
    fun: Incomplete
    args: Incomplete
    kwargs: Incomplete
    tempdir: Incomplete
    RETVAL: Incomplete
    STDOUT: Incomplete
    STDERR: Incomplete
    pid: Incomplete
    def __init__(
        self,
        fun: Incomplete,
        args: Incomplete | None = ...,
        kwargs: Incomplete | None = ...,
        nice_level: int = ...,
        child_on_start: Incomplete | None = ...,
        child_on_exit: Incomplete | None = ...,
    ) -> None: ...
    def waitfinish(self, waiter: Incomplete = ...) -> Incomplete: ...
    def __del__(self) -> None: ...

class Result:
    exitstatus: Incomplete
    signal: Incomplete
    retval: Incomplete
    out: Incomplete
    err: Incomplete
    def __init__(
        self,
        exitstatus: Incomplete,
        signal: Incomplete,
        retval: Incomplete,
        stdout: Incomplete,
        stderr: Incomplete,
    ) -> None: ...
