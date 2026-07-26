# AGENTS.md

Based on `CLAUDE.md`, corrected and condensed. Commands verified against actual source.

## Quick start

```bash
uv sync                       # install deps (uses uv, not pip)
uv run media-sorter ~/src ~/dst  # run CLI
uv run pytest tests/ -v --tb=short  # full test suite
uv run pytest tests/test_core.py -k test_parse_date_from_filename -vv  # single test
pre-commit run --all-files    # ruff lint + format, uv-lock sync
just upgrade                  # uv lock --upgrade
```

## Architecture

```
src/
├── cli.py      # CLI entrypoint (Typer app), calls process_files()
├── core.py     # EXIF date → filename fallback, file move/copy, ThreadPoolExecutor
├── logger.py   # init_logger(), log_message()
├── utils.py    # validate_directories(), print_param(), validate_path()
└── config.py   # DATE_FORMATS (has duplicate entry), EXIF_DATE_TAG
```

- **Source must exist** (Typer callback `validate_path`); **destination is auto-created**
- **Date priority**: EXIF DateTime tag → filename pattern matching → skip (logged as "SKIPPED")
- **Output dirs**: `destination/YYYY/MM/`
- **Parallel**: `ThreadPoolExecutor(max_workers=workers)`, default 8, CLI range 1–32
- **Tests**: in `tests/`, imports from `src.xxx` **inline** inside each test function (not at module top)
- **Lazy imports**: `core.py` does `from src.config import ...` inside functions (not module-level)
- **Log file**: defaults to `log.txt` inside destination directory

## Quirks / watch points

- `--copy` → `shutil.copy()`, default → `shutil.move()`
- `src/config.py` `DATE_FORMATS` list has `"%Y%m%d%H%M%S"` duplicated (line 2 and line 10)
- No pyproject.toml pytest config — pure defaults
- Requires Python `>=3.12` (`.python-version` is 3.14); README badge wrongly says "3.10+"
- `pre-commit` runs ruff-check, ruff-format, uv-lock, uv-export
- Individual file failures log an error but do not stop the batch

## .venv rules

- **Never** run `uv sync`, `uv lock`, `pip install`, or any command that modifies `.venv` without explicit user request.
- Always use `uv run` to invoke Python, pytest, or the app — this ensures the existing `.venv` is used.
- The `.venv/` directory is in `.claudeignore` — do not write files into it.
