from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image


def test_extract_exif_date(tmp_path: Path):
    from src.core import extract_exif_date

    img_file = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100))
    exif = img.getexif()
    exif[0x0132] = "2023:01:15 12:30:45"
    img.save(img_file, exif=exif.tobytes())

    result = extract_exif_date(img_file)
    assert result is not None
    assert result == datetime(2023, 1, 15, 12, 30, 45)


def test_extract_exif_date_no_exif(tmp_path: Path):
    from src.core import extract_exif_date

    img_file = tmp_path / "no_exif.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    result = extract_exif_date(img_file)
    assert result is None


def test_extract_exif_date_invalid_file(tmp_path: Path):
    from src.core import extract_exif_date

    text_file = tmp_path / "not_an_image.txt"
    text_file.write_text("not an image")

    result = extract_exif_date(text_file)
    assert result is None


def test_parse_date_from_filename_yyyymmdd():
    from src.core import parse_date_from_filename

    result = parse_date_from_filename("20230115_abc.jpg")
    assert result is not None
    assert result == datetime(2023, 1, 15)


def test_parse_date_from_filename_yyyymmdd_hhmmss():
    from src.core import parse_date_from_filename

    result = parse_date_from_filename("20230115_123045.jpg")
    assert result is not None
    assert result == datetime(2023, 1, 15, 12, 30, 45)


def test_parse_date_from_filename_with_dashes():
    from src.core import parse_date_from_filename

    result = parse_date_from_filename("2023-01-15 photo.png")
    assert result is not None
    assert result == datetime(2023, 1, 15)


def test_parse_date_from_filename_dd_mm_yyyy():
    from src.core import parse_date_from_filename

    result = parse_date_from_filename("15.01.2023.jpg")
    assert result is not None
    assert result == datetime(2023, 1, 15)


def test_parse_date_from_filename_no_date():
    from src.core import parse_date_from_filename

    result = parse_date_from_filename("image.jpg")
    assert result is None


def test_process_file_move(tmp_path: Path):
    from src.core import process_file

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    img_file = source_dir / "20230115_photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    result = process_file(
        "20230115_photo.jpg",
        source_dir,
        dest_dir,
        log_file,
        copy=False,
        dry_run=False,
    )
    assert result is True
    assert not img_file.exists()
    assert (dest_dir / "2023" / "01" / "20230115_photo.jpg").exists()


def test_process_file_copy(tmp_path: Path):
    from src.core import process_file

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    img_file = source_dir / "20230115_photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    result = process_file(
        "20230115_photo.jpg",
        source_dir,
        dest_dir,
        log_file,
        copy=True,
        dry_run=False,
    )
    assert result is True
    assert img_file.exists()
    assert (dest_dir / "2023" / "01" / "20230115_photo.jpg").exists()


def test_process_file_dry_run(tmp_path: Path):
    from src.core import process_file

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    img_file = source_dir / "20230115_photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    result = process_file(
        "20230115_photo.jpg",
        source_dir,
        dest_dir,
        log_file,
        copy=False,
        dry_run=True,
    )
    assert result is True
    assert img_file.exists()
    assert not (dest_dir / "2023" / "01" / "20230115_photo.jpg").exists()


def test_process_file_no_date(tmp_path: Path):
    from src.core import process_file

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    img_file = source_dir / "photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    result = process_file(
        "photo.jpg",
        source_dir,
        dest_dir,
        log_file,
        copy=False,
        dry_run=False,
    )
    assert result is None


def test_process_file_error(tmp_path: Path):
    from src.core import process_file

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    result = process_file(
        "nonexistent.jpg",
        source_dir,
        dest_dir,
        log_file,
        copy=False,
        dry_run=False,
    )
    assert result is False


def test_process_files(tmp_path: Path):
    from src.core import process_files

    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    log_file = tmp_path / "log.txt"

    filenames = ["20230101_a.jpg", "20230102_b.jpg", "20230103_c.jpg"]
    for name in filenames:
        Image.new("RGB", (100, 100)).save(source_dir / name)

    with patch("src.core.Progress") as mock_progress_cls:
        mock_progress = MagicMock()
        mock_progress_cls.return_value = mock_progress
        mock_progress.__enter__.return_value = mock_progress
        mock_progress.add_task.return_value = 0

        process_files(
            filenames,
            source_dir,
            dest_dir,
            workers=2,
            log_file=log_file,
            copy=False,
            dry_run=False,
        )

    for name in filenames:
        assert (dest_dir / "2023" / "01" / name).exists()
        assert not (source_dir / name).exists()
