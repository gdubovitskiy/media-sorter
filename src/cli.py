from pathlib import Path

import typer

from .core import process_files
from .logger import init_logger
from .utils import print_param, validate_directories, validate_path

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

    # Вывод параметров с иконками
    typer.echo("\n" + typer.style("CONFIGURATION", fg=typer.colors.BLUE, bold=True))
    print_param("Source directory", source, "📁", typer.colors.CYAN)
    print_param("Target directory", destination, "📂", typer.colors.CYAN)
    print_param("Log file path", log_file_path, "📝")
    print_param("Worker threads", workers, "👷", typer.colors.YELLOW)
    print_param("Operation mode", "COPY" if copy else "MOVE", "📋" if copy else "🚚", typer.colors.MAGENTA)
    print_param(
        "Dry run",
        "ENABLED" if dry_run else "DISABLED",
        "🛑" if dry_run else "✅",
        typer.colors.RED if dry_run else typer.colors.GREEN,
    )
    print_param("Files to process", len(files), "📄", typer.colors.BRIGHT_BLUE)
    typer.echo("")

    # Обработка файлов
    process_files(files, source, destination, workers, log_file_path, copy, dry_run)

    # Результат
    success_msg = typer.style("✅ SUCCESS! ", fg=typer.colors.GREEN, bold=True)
    log_msg = typer.style(f"Check logs in {log_file_path}", fg=typer.colors.BLUE)
    typer.echo(f"\n{success_msg}{log_msg}")


if __name__ == "__main__":
    app()
