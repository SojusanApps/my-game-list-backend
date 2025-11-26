import dataclasses
from typing import ClassVar
from _typeshed import Incomplete
from textual.app import ComposeResult as ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input
from trogon.introspect import (
    ArgumentSchema as ArgumentSchema,
    CommandName as CommandName,
    CommandSchema as CommandSchema,
    OptionSchema as OptionSchema,
)
from trogon.run_command import (
    UserArgumentData as UserArgumentData,
    UserCommandData as UserCommandData,
    UserOptionData as UserOptionData,
)
from trogon.widgets.parameter_controls import ParameterControls as ParameterControls

@dataclasses.dataclass
class FormControlMeta:
    widget: Widget
    meta: OptionSchema | ArgumentSchema

class CommandForm(Widget):
    DEFAULT_CSS: ClassVar[str]

    class Changed(Message):
        command_data: Incomplete
        def __init__(self, command_data: UserCommandData) -> None: ...

    command_schema: Incomplete
    command_schemas: Incomplete
    first_control: ParameterControls | None
    def __init__(
        self,
        command_schema: CommandSchema | None = None,
        command_schemas: dict[CommandName, CommandSchema] | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None: ...
    def compose(self) -> ComposeResult: ...
    def on_mount(self) -> None: ...
    def on_input_changed(self) -> None: ...
    def on_select_changed(self) -> None: ...
    def on_checkbox_changed(self) -> None: ...
    def on_multiple_choice_changed(self) -> None: ...
    def focus(self, scroll_visible: bool = True) -> Incomplete: ...
    def apply_filter(self, event: Input.Changed) -> None: ...
