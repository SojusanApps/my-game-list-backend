from _typeshed import Incomplete
from typing import ClassVar
from textual.app import ComposeResult as ComposeResult
from textual.screen import ModalScreen
from textual.widgets import DataTable, Tabs
from textual.reactive import Reactive
from textual.widgets.data_table import CursorType
from trogon.introspect import CommandSchema as CommandSchema
from trogon.widgets.multiple_choice import NonFocusableVerticalScroll as NonFocusableVerticalScroll

class CommandMetadata(DataTable[Incomplete]):
    show_header: bool
    zebra_stripes: bool
    cursor_type: Reactive[CursorType]
    command_schema: Incomplete
    def __init__(
        self,
        command_schema: CommandSchema,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None: ...
    def on_mount(self) -> None: ...

class CommandInfo(ModalScreen[Incomplete]):
    COMPONENT_CLASSES: ClassVar[Incomplete]
    BINDINGS: ClassVar[Incomplete]
    command_schema: Incomplete
    def __init__(
        self, command_schema: CommandSchema, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None: ...
    def compose(self) -> ComposeResult: ...
    def switch_content(self, event: Tabs.TabActivated) -> None: ...
    def action_close_modal(self) -> None: ...
