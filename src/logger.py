from datetime import datetime
from pathlib import Path


def init_logger(log_file: Path) -> None:
    """Инициализация логгера с гарантированным созданием директорий."""
    try:
        # Создаем все родительские директории
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Создаем/очищаем файл
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] LOG INITIALIZED\n")
    except Exception as e:
        print(f"⚠️ Failed to initialize logger: {str(e)}")
        raise


def log_message(message: str, log_file: Path) -> None:
    """Запись сообщения в лог."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
