from _typeshed import Incomplete
from asyncio.events import AbstractEventLoop
from django.core.management import BaseCommand
from django_tui.management.commands.ish import InteractiveShellScreen as InteractiveShellScreen
from textual.app import App, AutopilotCallbackType as AutopilotCallbackType, ComposeResult as ComposeResult, ReturnType
from textual.binding import BindingType
from textual.screen import Screen
from textual.widgets import Tree
from textual.widgets.tree import TreeNode as TreeNode
from trogon.introspect import CommandSchema
from trogon.run_command import UserCommandData as UserCommandData
from trogon.widgets.about import TextDialog
from trogon.widgets.form import CommandForm
from typing import Any, Literal, ClassVar

def introspect_django_commands() -> dict[str, CommandSchema]: ...

class AboutDialog(TextDialog):
    DEFAULT_CSS: ClassVar[str]
    def __init__(self) -> None: ...

class DjangoCommandBuilder(Screen[Incomplete]):
    COMPONENT_CLASSES: ClassVar[set[str]]
    BINDINGS: ClassVar[list[BindingType]]
    command_data: Incomplete
    is_grouped_cli: bool
    command_schemas: Incomplete
    click_app_name: Incomplete
    command_name: Incomplete
    version: Incomplete
    highlighter: Incomplete
    def __init__(
        self,
        click_app_name: str,
        command_name: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None: ...
    def compose(self) -> ComposeResult: ...
    def action_close_and_run(self) -> None: ...
    async def selected_command_changed(self, event: Tree.NodeHighlighted[CommandSchema]) -> None: ...
    def update_command_data(self, event: CommandForm.Changed) -> None: ...

class DjangoTui(App[Incomplete]):
    CSS_PATH: ClassVar[str]
    BINDINGS: ClassVar[list[BindingType]]
    post_run_command: list[str]
    is_grouped_cli: bool
    execute_on_exit: bool
    app_name: str
    command_name: str
    open_shell: Incomplete
    def __init__(self, *, open_shell: bool = False) -> None: ...
    def get_default_screen(self) -> DjangoCommandBuilder: ...
    def on_button_pressed(self) -> None: ...
    def run(
        self,
        *,
        headless: bool = False,
        inline: bool = False,
        inline_no_clear: bool = False,
        mouse: bool = True,
        size: tuple[int, int] | None = None,
        auto_pilot: AutopilotCallbackType | None = None,
        loop: AbstractEventLoop | None = None,
    ) -> ReturnType | None: ...
    def update_command_to_run(self, event: CommandForm.Changed) -> None: ...
    def action_focus_command_tree(self) -> None: ...
    def action_show_command_info(self) -> None: ...
    def action_visit(self, url: str) -> None: ...
    def action_select_mode(self, mode_id: Literal["commands", "shell"]) -> None: ...
    def action_copy_command(self) -> None: ...
    def action_about(self) -> None: ...

class Command(BaseCommand):
    help: str
    def add_arguments(self, parser: Incomplete) -> None: ...
    def handle(self, *args: Any, shell: bool = False, **options: Any) -> None: ...
