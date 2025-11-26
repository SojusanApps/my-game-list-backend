from dataclasses import dataclass, field
from rich.text import Text
from trogon.introspect import (
    ArgumentSchema as ArgumentSchema,
    CommandName as CommandName,
    CommandSchema as CommandSchema,
    MultiValueParamData as MultiValueParamData,
    OptionSchema as OptionSchema,
)
from trogon.widgets.parameter_controls import ValueNotSupplied as ValueNotSupplied
from typing import Any

@dataclass
class UserOptionData:
    name: str | list[str]
    value: tuple[Any]
    option_schema: OptionSchema
    @property
    def string_name(self) -> str: ...

@dataclass
class UserArgumentData:
    name: str
    value: tuple[Any]
    argument_schema: ArgumentSchema

@dataclass
class UserCommandData:
    name: CommandName
    options: list[UserOptionData] = field(default_factory=list)
    arguments: list[UserArgumentData] = field(default_factory=list)
    subcommand: UserCommandData | None = ...
    parent: UserCommandData | None = ...
    command_schema: CommandSchema | None = ...
    def to_cli_args(self, include_root_command: bool = False) -> list[str]: ...
    def to_cli_string(self, include_root_command: bool = False) -> Text: ...
