import datetime
from pathlib import Path

_APP = Path(__file__).resolve().parent.parent
_DATA = _APP / "data"
_DATA.mkdir(parents=True, exist_ok=True)
LOG_FILE = str(_DATA / "promind7_local.log")


def _write(level: str, message: str):
    """Ecrit une entrée de log dans promind7_local.log avec timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass  # jamais d'erreur de log


def log_info(message: str):
    _write("INFO", message)


def log_warn(message: str):
    _write("WARN", message)


def log_error(message: str):
    _write("ERROR", message)
