from .. import constants as constants
from _typeshed import Incomplete
from typing import ClassVar
from rich.text import TextType as TextType
from textual.app import ComposeResult as ComposeResult
from textual.screen import ModalScreen
from textual.widgets._button import ButtonVariant as ButtonVariant

class TextDialog(ModalScreen[None]):
    DEFAULT_CSS: ClassVar[str]
    BINDINGS: ClassVar[Incomplete]
    def __init__(self, title: TextType, message: TextType) -> None: ...
    @property
    def button_style(self) -> ButtonVariant: ...
    def compose(self) -> ComposeResult: ...
    def on_mount(self) -> None: ...
    def on_button_pressed(self) -> None: ...

class AboutDialog(TextDialog):
    DEFAULT_CSS: ClassVar[str]
    def __init__(self) -> None: ...
