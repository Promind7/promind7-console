import os
import sqlite3
from pathlib import Path


def get_db_path() -> str:
    env = (os.getenv("PROMIND7_DB_PATH") or "").strip()
    if env:
        return env
    root = Path(__file__).resolve().parent.parent
    data = root / "app" / "data"
    data.mkdir(parents=True, exist_ok=True)
    return str(data / "promind7.db")

def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn
