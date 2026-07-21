import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from tqdm import tqdm

from .logger import log_message


def extract_exif_date(filepath: Path) -> Optional[datetime]:
    """Extracts the date from the image's EXIF DateTime tag.

    Args:
        filepath (Path): Path to the image file.

    Returns:
        Optional[datetime]: Extracted datetime if successful, otherwise None.

    Example:
        >>> date = extract_exif_date(Path("image.jpg"))
        >>> print(date)
        2023-01-15 12:30:45
    """
    from src.config import EXIF_DATE_TAG

    try:
        with Image.open(filepath) as img:
            exif = img.getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == EXIF_DATE_TAG and value:
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except (UnidentifiedImageError, AttributeError, ValueError):
        return None
    return None


def parse_date_from_filename(filename: str) -> Optional[datetime]:
    """Attempts to parse date from filename using predefined formats.

    Args:
        filename (str): The filename to parse.

    Returns:
        Optional[datetime]: Parsed datetime if successful, otherwise None.

    Example:
        >>> date = parse_date_from_filename("20230115_123045.jpg")
        >>> print(date)
        2023-01-15 12:30:45
    """
    from src.config import DATE_FORMATS

    base_name = Path(filename).stem
    # fmt: off
    clean_name = (
        base_name
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace(".", "")
    )
    # fmt: on

    for fmt in ["%Y%m%d%H%M%S", "%Y%m%d"]:
        try:
            return datetime.strptime(clean_name[: len(fmt)].ljust(len(fmt), "0"), fmt)
        except ValueError:
            continue

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(base_name[: len(fmt)], fmt)
        except ValueError:
            continue

    return None


def process_file(
    filename: str,
    source_dir: Path,
    dest_dir: Path,
    log_file: Path,
    copy: bool = False,
    dry_run: bool = False,
) -> Optional[bool]:
    """Processes a single file by organizing it into date-based directory structure.

    Args:
        filename (str): Name of the file to process.
        source_dir (Path): Source directory path.
        dest_dir (Path): Destination directory path.
        log_file (Path): Path to log file.
        copy (bool): If True, copies instead of moving. Defaults to False.
        dry_run (bool): If True, only logs actions without executing. Defaults to False.

    Returns:
        Optional[bool]: True if successful, None if skipped, False if error.

    Raises:
        Exception: Logs any processing errors to the log file.

    Example:
        >>> success = process_file("photo.jpg", Path("/src"), Path("/dest"), Path("log.txt"))
    """
    try:
        filepath = source_dir / filename

        date = extract_exif_date(filepath)
        source = "EXIF"

        if date is None:
            date = parse_date_from_filename(filename)
            if date is None:
                log_message(f"SKIPPED: No date found in {filename}", log_file)
                return None
            source = "filename"

        year, month = date.year, f"{date.month:02d}"
        dest_path = dest_dir / str(year) / month / filename

        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if copy:
                shutil.copy(str(filepath), str(dest_path))  # Copy file
            else:
                shutil.move(str(filepath), str(dest_path))  # Move file

        status = "DRY RUN" if dry_run else "MOVED" if not copy else "COPIED"
        log_message(
            f"{status:<10} ({source:^10}): {filename:<30} -> {year}/{month}",
            log_file,
        )
        return True

    except Exception as e:
        log_message(f"ERROR processing {filename}: {str(e)}", log_file)
        return False


def process_files(
    files: List[str],
    source_dir: Path,
    dest_dir: Path,
    workers: int = 8,
    log_file: Path = Path("log.txt"),
    copy: bool = False,
    dry_run: bool = False,
) -> None:
    """Processes multiple files in parallel with progress tracking.

    Args:
        files (List[str]): List of filenames to process.
        source_dir (Path): Source directory path.
        dest_dir (Path): Destination directory path.
        workers (int): Number of worker threads. Defaults to 8.
        log_file (Path): Path to log file. Defaults to "log.txt".
        copy (bool): Copy files if True. Defaults to False.
        dry_run (bool): Simulate processing if True. Defaults to False.

    Example:
        >>> process_files(["1.jpg", "2.jpg"], Path("/src"), Path("/dest"))
    """
    with tqdm(total=len(files), desc="Processing files") as pbar:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    process_file,
                    filename,
                    source_dir,
                    dest_dir,
                    log_file,
                    copy,
                    dry_run,
                ): filename
                for filename in files
            }

            for future in as_completed(futures):
                future.result()
                pbar.update(1)
                pbar.set_postfix_str(f"Last: {futures[future]}", refresh=False)
