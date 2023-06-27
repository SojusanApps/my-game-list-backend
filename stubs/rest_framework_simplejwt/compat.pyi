from _typeshed import Incomplete
from django.urls import reverse as reverse, reverse_lazy as reverse_lazy

class RemovedInDjango20Warning(DeprecationWarning): ...

class CallableBool:
    do_not_call_in_templates: bool
    value: Incomplete
    def __init__(self, value: Incomplete) -> None: ...
    def __bool__(self) -> bool: ...
    def __call__(self) -> Incomplete: ...
    def __nonzero__(self) -> Incomplete: ...
    def __eq__(self, other: Incomplete) -> Incomplete: ...
    def __ne__(self, other: Incomplete) -> Incomplete: ...
    def __or__(self, other: Incomplete) -> Incomplete: ...
    def __hash__(self) -> Incomplete: ...

CallableFalse: Incomplete
CallableTrue: Incomplete
