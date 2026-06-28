# 📂 Media Sorter by Date

**Automatically organize files into `YYYY/MM` folders based on dates in filenames**
*(Perfect for photos, documents, and any files with EXIF-data or pattern filename)*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Typer CLI](https://img.shields.io/badge/CLI-Typer-FF4785)](https://typer.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Parallel processing** with configurable worker threads (4-32)
- 📅 **Smart date detection** from EXIF-data or filenames pattern
- 📊 **Visual progress tracking** with tqdm
- 🧪 **Dry-run mode** for safe testing
- 📝 **Detailed logging** of all operations
- ✔️ **Automatic directory validation**
- 🛠️ **Error handling** with clear messages
- 📂 **File copying option** in addition to moving files

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)

### Installation
```bash
# Clone repository
git clone https://github.com/gdubovitskiy/media-sorter.git
cd media-sorter

# Install dependencies with uv
uv sync
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
```bash
Options:
  --workers, -w INTEGER  Number of parallel threads [4-32] (default: 8)
  --log, -l TEXT         Name of log file (default: log.txt)
  --dry-run              Simulation mode (no actual file moves)
  --copy                 Copy files instead of moving them
  --help                 Show this message and exit
```

## 🧠 How It Works

1. **Scans** source directory for files matching `YYYYMMDD_*` pattern
2. **Validates** directory permissions and existence
3. **Creates** folder structure `Destination/YYYY/MM/`
4. **Moves or copies** files with parallel processing
5. **Logs** all actions with timestamps

## 🛠️ Project Structure

```
src/
├── cli.py          # Command-line interface (Typer)
├── core.py         # Main processing logic
├── logger.py       # Logging utilities
└── utils.py        # Directory validation
```

## 🐛 Troubleshooting

### Common Issues
1. **uv command not found**:
   ```bash
   # Install uv if not already installed
   pip install uv
   # or use: curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **No files found**:
   - Ensure filenames contain dates in `YYYYMMDD_*` format
   - Check source directory permissions

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
cat sorting_log.txt

# 3. Run for real with 8 threads
uv run media-sorter ~/DCIM/Camera ~/Photos/Organized --workers 8

# 4. Run with copy option
uv run media-sorter ~/DCIM/Camera ~/Photos/Organized --copy
```
