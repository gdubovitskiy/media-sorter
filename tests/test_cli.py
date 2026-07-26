from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image


def test_main_integration(tmp_path: Path):
    from src.cli import main

    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()

    img_file = source / "photo.jpg"
    img = Image.new("RGB", (100, 100))
    exif = img.getexif()
    exif[0x0132] = "2023:06:15 10:30:00"
    img.save(img_file, exif=exif.tobytes())

    with patch("typer.echo"):
        main(
            source,
            dest,
            workers=1,
            log_file=Path("test.log"),
            copy=False,
            dry_run=False,
        )

    assert (dest / "2023" / "06" / "photo.jpg").exists()
    assert not img_file.exists()


def test_main_dry_run(tmp_path: Path):
    from src.cli import main

    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()

    img_file = source / "20230615_photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    with patch("typer.echo"):
        main(
            source, dest, workers=1, log_file=Path("test.log"), copy=False, dry_run=True
        )

    assert img_file.exists()
    assert not (dest / "2023" / "06" / "20230615_photo.jpg").exists()


def test_main_copy(tmp_path: Path):
    from src.cli import main

    source = tmp_path / "source"
    dest = tmp_path / "dest"
    source.mkdir()

    img_file = source / "20230615_photo.jpg"
    Image.new("RGB", (100, 100)).save(img_file)

    with patch("typer.echo"):
        main(
            source, dest, workers=1, log_file=Path("test.log"), copy=True, dry_run=False
        )

    assert (dest / "2023" / "06" / "20230615_photo.jpg").exists()
    assert img_file.exists()
