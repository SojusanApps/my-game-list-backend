import click
from _typeshed import Incomplete
from textual import events as events, log as log
from textual.app import App, AutopilotCallbackType as AutopilotCallbackType, ComposeResult as ComposeResult
from textual.binding import BindingType
from textual.screen import Screen
from textual.widgets import Tree
from textual.widgets.tree import TreeNode as TreeNode
from trogon.detect_run_string import detect_run_string as detect_run_string
from trogon.introspect import (
    CommandName as CommandName,
    CommandSchema as CommandSchema,
    introspect_click_app as introspect_click_app,
)
from trogon.run_command import UserCommandData as UserCommandData
from trogon.widgets.command_info import CommandInfo as CommandInfo
from trogon.widgets.command_tree import CommandTree as CommandTree
from trogon.widgets.form import CommandForm as CommandForm
from trogon.widgets.multiple_choice import NonFocusableVerticalScroll as NonFocusableVerticalScroll
from typing import Any, ClassVar

class CommandBuilder(Screen[None]):
    COMPONENT_CLASSES: ClassVar[set[str]]
    BINDINGS: ClassVar[list[BindingType]]
    command_data: UserCommandData
    cli: Incomplete
    is_grouped_cli: Incomplete
    command_schemas: Incomplete
    click_app_name: Incomplete
    command_name: Incomplete
    version: Incomplete
    highlighter: Incomplete
    def __init__(
        self,
        cli: Any,
        click_app_name: str,
        command_name: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None: ...
    def compose(self) -> ComposeResult: ...
    def action_close_and_run(self) -> None: ...
    def action_about(self) -> None: ...
    async def selected_command_changed(self, event: Tree.NodeHighlighted[CommandSchema]) -> None: ...
    def update_command_data(self, event: CommandForm.Changed) -> None: ...

class Trogon(App[None]):
    CSS_PATH: ClassVar[Incomplete]
    cli: Incomplete
    post_run_command: list[str]
    is_grouped_cli: Incomplete
    execute_on_exit: bool
    app_name: Incomplete
    command_name: Incomplete
    def __init__(
        self,
        cli: click.Group | click.Command,
        app_name: str | None = None,
        command_name: str = "tui",
        click_context: click.Context | None = None,
    ) -> None: ...
    def get_default_screen(self) -> CommandBuilder: ...
    def on_button_pressed(self) -> None: ...
    def run(
        self,
        *args: Any,
        headless: bool = False,
        size: tuple[int, int] | None = None,
        auto_pilot: AutopilotCallbackType | None = None,
        **kwargs: Any,
    ) -> None: ...
    def update_command_to_run(self, event: CommandForm.Changed) -> Incomplete: ...
    def action_focus_command_tree(self) -> None: ...
    def action_show_command_info(self) -> None: ...
    def action_visit(self, url: str) -> None: ...

def tui(name: str | None = None, command: str = "tui", help: str = "Open Textual TUI.") -> Incomplete: ...
