from _typeshed import Incomplete
from rich.text import Text
from textual.app import ComposeResult as ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input, Select
from trogon.introspect import (
    ArgumentSchema as ArgumentSchema,
    MultiValueParamData as MultiValueParamData,
    OptionSchema as OptionSchema,
)
from trogon.widgets.multiple_choice import MultipleChoice as MultipleChoice
from typing import Any, Callable, Iterable

ControlWidgetType = Input | Checkbox | MultipleChoice | Select[str]

class ControlGroup(Vertical): ...
class ControlGroupsContainer(Vertical): ...

class ValueNotSupplied:
    def __eq__(self, other: Incomplete) -> Incomplete: ...
    def __lt__(self, other: Incomplete) -> Incomplete: ...
    def __bool__(self) -> bool: ...

class ParameterControls(Widget):
    schema: Incomplete
    first_control: Widget | None
    def __init__(
        self,
        schema: ArgumentSchema | OptionSchema,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None: ...
    display: Incomplete
    def apply_filter(self, filter_query: str) -> bool: ...
    def compose(self) -> ComposeResult: ...
    def make_widget_group(self) -> Iterable[ControlWidgetType]: ...
    def add_another_widget_group(self, event: Button.Pressed) -> None: ...
    def get_values(self) -> MultiValueParamData: ...
    def get_control_method(
        self, argument_type: Any
    ) -> Callable[[Any, Text, bool, OptionSchema | ArgumentSchema, str], ControlWidgetType]: ...
    @staticmethod
    def make_text_control(
        default: Any, label: Text | None, multiple: bool, schema: OptionSchema | ArgumentSchema, control_id: str
    ) -> Iterable[ControlWidgetType]: ...
    @staticmethod
    def make_checkbox_control(
        default: MultiValueParamData,
        label: Text | None,
        multiple: bool,
        schema: OptionSchema | ArgumentSchema,
        control_id: str,
    ) -> Iterable[ControlWidgetType]: ...
    @staticmethod
    def make_choice_control(
        default: MultiValueParamData,
        label: Text | None,
        multiple: bool,
        schema: OptionSchema | ArgumentSchema,
        control_id: str,
        choices: list[str],
    ) -> Iterable[ControlWidgetType]: ...
    def focus(self, scroll_visible: bool = True) -> Incomplete: ...
