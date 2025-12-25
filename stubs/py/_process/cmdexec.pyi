from py._error import Error
from _typeshed import Incomplete
from subprocess import PIPE as PIPE, Popen as Popen

def cmdexec(cmd: Incomplete) -> Incomplete: ...

class ExecutionFailed(Error):
    status: Incomplete
    systemstatus: Incomplete
    cmd: Incomplete
    err: Incomplete
    out: Incomplete
    def __init__(
        self,
        status: Incomplete,
        systemstatus: Incomplete,
        cmd: Incomplete,
        out: Incomplete,
        err: Incomplete,
    ) -> None: ...
