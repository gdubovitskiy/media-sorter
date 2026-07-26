from pathlib import Path

import typer
from rich import box
from rich.panel import Panel
from rich.table import Table

from .core import process_files
from .logger import init_logger
from .utils import console, validate_directories, validate_path

app = typer.Typer()


@app.command()
def main(
    source: Path = typer.Argument(  # noqa: B008
        ...,
        help="📁 Source directory with files",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        callback=validate_path,
    ),
    destination: Path = typer.Argument(  # noqa: B008
        ...,
        help="📂 Target directory for organized files",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        callback=validate_path,
    ),
    workers: int = typer.Option(8, "--workers", "-w", help="Number of parallel threads", min=1, max=32),
    log_file: Path = typer.Option("log.txt", "--log", "-l", help="Path to log file"),  # noqa: B008
    copy: bool = typer.Option(False, "--copy", help="Copy files instead of moving them"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without moving files"),
):
    """Sort files from SOURCE to DESTINATION based on dates in filenames (YYYYMMDD_*)."""
    log_file_path = destination / log_file
    destination.mkdir(parents=True, exist_ok=True)
    init_logger(log_file_path)
    validate_directories(source, destination)
    files = [f.name for f in source.iterdir() if f.is_file()]

    table = Table.grid(padding=(0, 2), expand=True)
    table.add_row("📁  [bold]Source directory:[/]",  f"[cyan]{source}[/]")
    table.add_row("📂  [bold]Target directory:[/]",  f"[cyan]{destination}[/]")
    table.add_row("📝  [bold]Log file path:[/]",     f"{log_file_path}")
    table.add_row("👷  [bold]Worker threads:[/]",    f"[yellow]{workers}[/]")
    mode_str, mode_icon = ("COPY", "📋") if copy else ("MOVE", "🚚")
    table.add_row(f"{mode_icon}  [bold]Operation mode:[/]", f"[magenta]{mode_str}[/]")
    dry_str, dry_icon = ("ENABLED", "🛑") if dry_run else ("DISABLED", "✅")
    dry_color = "red" if dry_run else "green"
    table.add_row(f"{dry_icon}  [bold]Dry run:[/]",  f"[{dry_color}]{dry_str}[/]")
    table.add_row("📄  [bold]Files to process:[/]", f"[bright_blue]{len(files)}[/]")

    panel = Panel(
        table,
        title="[bold blue]CONFIGURATION[/]",
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()

    process_files(files, source, destination, workers, log_file_path, copy, dry_run, console=console)

    console.print(f"\n[bold green]✅ SUCCESS![/] [blue]Check logs in {log_file_path}[/]")


if __name__ == "__main__":
    app()
