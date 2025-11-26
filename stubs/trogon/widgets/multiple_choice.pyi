from _typeshed import Incomplete
from rich.text import TextType as TextType
from textual.app import ComposeResult as ComposeResult
from textual.binding import BindingType as BindingType
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Checkbox
from typing import Any, ClassVar

class NonFocusableVerticalScroll(VerticalScroll, can_focus=False): ...

class MultipleChoice(Widget):
    DEFAULT_CSS: ClassVar[str]
    BINDINGS: ClassVar[list[BindingType]]
    options: Incomplete
    defaults: Incomplete
    selected: Incomplete
    def __init__(
        self,
        options: list[TextType],
        defaults: list[tuple[Any]] | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None: ...

    class Changed(Message):
        selected: Incomplete
        def __init__(self, selected: list[Checkbox]) -> None: ...

    def compose(self) -> ComposeResult: ...
    def checkbox_toggled(self) -> None: ...
    def select_by_label(self, label: str) -> None: ...
    def action_next_button(self) -> None: ...
    def action_previous_button(self) -> None: ...
