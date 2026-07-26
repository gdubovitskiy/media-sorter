from pathlib import Path
from typing import Any, Optional

import typer
from rich.console import Console

console = Console()


def validate_directories(source: Path, destination: Path) -> None:
    """Проверка директорий."""
    if not source.exists():
        raise FileNotFoundError(f"Директория не найдена: {source}")
    destination.mkdir(parents=True, exist_ok=True)


def print_param(label: str, value: Any, icon: Optional[str] = None, color: Optional[str] = None):
    """Печатает параметр с иконкой и стилем через Rich."""
    icon_part = f"{icon}  " if icon else ""
    if color:
        console.print(f"{icon_part}[bold]{label}:[/] [{color}]{value}[/]")
    else:
        console.print(f"{icon_part}[bold]{label}:[/] {value}")


def validate_path(ctx: typer.Context, value: Path) -> Path:
    if not value.exists() and ctx.params.get("source") is None:
        raise typer.BadParameter(f"🚨 Path {value} does not exist")
    return value
