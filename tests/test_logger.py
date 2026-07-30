from pathlib import Path

import pytest


def test_init_logger_creates_file(tmp_path: Path):
    from src.logger import init_logger

    log_file = tmp_path / "test.log"
    init_logger(log_file)
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "LOG INITIALIZED" in content


def test_init_logger_creates_parent_dirs(tmp_path: Path):
    from src.logger import init_logger

    log_file = tmp_path / "subdir" / "logs" / "test.log"
    init_logger(log_file)
    assert log_file.exists()


def test_log_message_appends(tmp_path: Path):
    from src.logger import init_logger, log_message

    log_file = tmp_path / "test.log"
    init_logger(log_file)
    log_message("First message", log_file)
    log_message("Second message", log_file)

    content = log_file.read_text(encoding="utf-8")
    assert "First message" in content
    assert "Second message" in content


def test_init_logger_exception(tmp_path: Path):
    from src.logger import init_logger

    log_file = tmp_path / "test.log"
    log_file.write_text("", encoding="utf-8")
    bad_path = log_file / "subdir" / "test.log"

    with pytest.raises((NotADirectoryError, FileNotFoundError, FileExistsError)):
        init_logger(bad_path)
