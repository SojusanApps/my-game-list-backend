from _typeshed import Incomplete
from typing import ClassVar
from rich.style import Style as Style
from rich.text import Text, TextType as TextType
from textual.widgets import Tree
from textual.widgets._tree import TreeNode as TreeNode
from trogon.introspect import CommandName as CommandName, CommandSchema as CommandSchema

class CommandTree(Tree[CommandSchema]):
    COMPONENT_CLASSES: ClassVar[Incomplete]
    show_root: bool
    guide_depth: int
    show_guides: bool
    cli_metadata: Incomplete
    command_name: Incomplete
    def __init__(self, label: TextType, cli_metadata: dict[CommandName, CommandSchema], command_name: str) -> None: ...
    def render_label(self, node: TreeNode[CommandSchema], base_style: Style, style: Style) -> Text: ...
    def on_mount(self) -> Incomplete: ...
