import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hotel.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection() -> sqlite3.Connection:
    """Подключение к SQLite с защитой связей и автовосстановлением базы."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # Если базы ещё нет или она пустая — автоматически создаём таблицы из schema.sql
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cur.fetchone() and os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
    except Exception:
        pass

    return conn