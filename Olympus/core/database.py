"""
Olympus V4.0 - Core Database Module
"""
import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
from contextlib import contextmanager

class OlympusDB:
    def __init__(self, db_path: str = "data/olympus.db"):
        self.db_path = db_path
        self._ensure_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    status TEXT DEFAULT 'stopped',
                    last_heartbeat TEXT,
                    pid INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    worker_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    result TEXT NOT NULL,
                    earnings REAL DEFAULT 0,
                    details TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    worker_name TEXT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)
    
    def log(self, message: str, level: str = "INFO", worker_name: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (timestamp, worker_name, level, message)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().isoformat(), worker_name, level, message))
    
    def register_worker(self, name: str, pid: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO workers (name, status, last_heartbeat, pid)
                VALUES (?, 'running', ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    status='running', last_heartbeat=?, pid=?
            """, (name, datetime.now().isoformat(), pid,
                  datetime.now().isoformat(), pid))
    
    def log_run(self, worker_name: str, result: str, **kwargs):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO runs (worker_name, timestamp, result, earnings, details)
                VALUES (?, ?, ?, ?, ?)
            """, (worker_name, datetime.now().isoformat(), result,
                  kwargs.get('earnings', 0), kwargs.get('details')))
    
    def get_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_runs,
                    SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins,
                    SUM(earnings) as total_earnings
                FROM runs
            """)
            row = cursor.fetchone()
            return dict(row) if row else {}

db = OlympusDB()
