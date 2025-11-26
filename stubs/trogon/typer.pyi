import typer
from trogon.trogon import Trogon as Trogon

def init_tui(app: typer.Typer, name: str | None = None) -> typer.Typer: ...
