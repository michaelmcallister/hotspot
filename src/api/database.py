import sqlite3
from pathlib import Path
from typing import Dict, Any


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def fetch_all(self, query: str, params: Dict[str, Any] = None):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()