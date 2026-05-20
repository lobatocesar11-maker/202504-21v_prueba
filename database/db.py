import sqlite3
from pathlib import Path

from flask import g


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "students.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                grade REAL NOT NULL,
                is_approved INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        db.commit()
