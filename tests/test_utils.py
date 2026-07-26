from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer


def test_validate_directories_source_exists(tmp_path: Path):
    from src.utils import validate_directories

    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"

    validate_directories(source, dest)
    assert dest.exists()


def test_validate_directories_source_not_found(tmp_path: Path):
    from src.utils import validate_directories

    source = tmp_path / "nonexistent"
    dest = tmp_path / "dest"

    with pytest.raises(FileNotFoundError):
        validate_directories(source, dest)


def test_validate_directories_creates_dest(tmp_path: Path):
    from src.utils import validate_directories

    source = tmp_path / "source"
    source.mkdir()
    dest = tmp_path / "dest"
    assert not dest.exists()

    validate_directories(source, dest)
    assert dest.exists()


def test_print_param_basic():
    from src.utils import print_param

    with patch("typer.echo") as mock_echo:
        print_param("Workers", 8)
        mock_echo.assert_called_once()


def test_print_param_with_icon_and_color():
    from src.utils import print_param

    with patch("typer.echo") as mock_echo:
        print_param("Mode", "COPY", icon="📋", color=typer.colors.MAGENTA)
        mock_echo.assert_called_once()


def test_validate_path_exists():
    from src.utils import validate_path

    ctx = MagicMock()
    ctx.params = {}
    existing = Path("/tmp")

    result = validate_path(ctx, existing)
    assert result == existing


def test_validate_path_not_exists():
    from src.utils import validate_path

    ctx = MagicMock()
    ctx.params = {}

    with pytest.raises(typer.BadParameter):
        validate_path(ctx, Path("/nonexistent_path_xyzzy_test"))
