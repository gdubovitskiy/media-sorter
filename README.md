# 📂 Media Sorter by Date

**Automatically organize files into `YYYY/MM` folders based on dates in filenames or EXIF metadata**
*(Perfect for photos, documents, and any files with EXIF-data or pattern filename)*

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Typer CLI](https://img.shields.io/badge/CLI-Typer-FF4785)](https://typer.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Parallel processing** with configurable worker threads (1-32)
- 📅 **Smart date detection** from EXIF-data (DateTime tag) or filename patterns
- 📊 **Visual progress tracking** with tqdm
- 🧪 **Dry-run mode** for safe testing
- 📝 **Detailed logging** with timestamps (saved in destination directory)
- ✔️ **Automatic directory creation** and validation
- 🛠️ **Error handling** with clear messages
- 📂 **File copying option** in addition to moving files

## ⚡ Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)

### Installation & Setup
```bash
# Clone repository
git clone https://github.com/gdubovitskiy/media-sorter.git
cd media-sorter

# Install dependencies and the package in editable mode
uv sync

# Run pre-commit hooks to lint/format code and sync uv.lock
pre-commit run --all-files
```

### Basic Usage
```bash
# Simple organization
uv run media-sorter ~/source_folder ~/destination_folder

# With progress display and logging
uv run media-sorter ~/Photos ~/Sorted --workers 4 --log migration.log

# Copy files instead of moving
uv run media-sorter ~/Photos ~/Sorted --copy
```

### Command Options
```
Options:
  --workers, -w INTEGER  Number of parallel threads (default: 8, range: 1-32)
  --log, -l FILE         Log file path (default: log.txt inside destination)
  --dry-run              Simulation mode (no actual file moves)
  --copy                 Copy files instead of moving them
  --help                 Show this message and exit
```

## 🧠 How It Works

1. **Scans** all files in the source directory
2. **Extracts date** for each file:
   - First tries EXIF `DateTime` tag (via Pillow)
   - Falls back to parsing filename against multiple date formats
   - Skips files with no detectable date (logged as "SKIPPED")
3. **Creates** folder structure `Destination/YYYY/MM/`
4. **Moves or copies** files with parallel processing (ThreadPoolExecutor)
5. **Logs** all actions with timestamps

## 🛠️ Project Structure

```
media-sorter/
├── src/                    # Application source code
│   ├── cli.py              # Command-line interface (Typer app)
│   ├── core.py             # EXIF extraction, filename parsing, file operations
│   ├── logger.py           # Logging utilities (init_logger, log_message)
│   ├── utils.py            # Directory validation, path helpers, param display
│   └── config.py           # Date format patterns and EXIF tag constant
├── tests/                  # Test suite (pytest)
│   ├── test_core.py        # Unit tests for core processing logic
│   ├── test_cli.py         # Integration tests for CLI
│   ├── test_logger.py      # Tests for logging utilities
│   └── test_utils.py       # Tests for validation and helpers
├── pyproject.toml          # Project config, dependencies, build settings
├── uv.lock                 # Locked dependency versions
├── .pre-commit-config.yaml # Pre-commit hooks (ruff, uv-lock)
├── .python-version         # Python version for uv
├── AGENTS.md               # Guidelines for AI coding assistants
├── CLAUDE.md               # Guidelines for Claude Code AI assistant
└── README.md               # This file
```

## 🛠️ Development & Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) for linting, formatting and dependency management:

```bash
# Run all hooks (lint + format)
pre-commit run --all-files

# Check UV lock file changes
pre-commit run uv-lock --files pyproject.toml
```

Available hooks:
- `ruff-check` - Lint with auto-fix
- `ruff-format` - Auto-format code
- `uv-lock` - Sync dependencies (ensures `uv.lock` stays up to date)

---

## 🐛 Troubleshooting

### Common Issues
1. **uv command not found**:
   ```bash
   pip install uv
   # or: curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **No files found**:
   - Ensure filenames contain supported date patterns (e.g. `20230115_abc.jpg`, `photo-2024-07-20.png`)
   - Check source directory permissions
   - Verify files have EXIF DateTime tag or parseable date in filename

3. **Permission errors**:
   ```bash
   # On Linux/Mac:
   chmod +x src/cli.py
   ```

---

### 🎯 Example Workflow

```bash
# 1. First do a dry-run
uv run media-sorter ~/DCIM/Camera ~/Photos/Organized --dry-run

# 2. Check the log
cat ~/Photos/Organized/log.txt

# 3. Run for real with 8 threads
uv run media-sorter ~/DCIM/Camera ~/Photos/Organized --workers 8

# 4. Run with copy option
uv run media-sorter ~/DCIM/Camera ~/Photos/Organized --copy
```
