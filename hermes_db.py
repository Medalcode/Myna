import os
import sqlite3
import threading
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'hermes.db')
_DB_LOCK = threading.Lock()

def _ensure_db():
    """Create the SQLite DB and the required table if they don't exist yet."""
    with _DB_LOCK:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                proxy TEXT,
                recipe TEXT,
                result TEXT,
                sats INTEGER,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()

def log_run(proxy: str, recipe: str, result: str, sats: int = 0, details: str = ""):
    """Insert a new row describing a single execution of a recipe.

    Parameters
    ----------
    proxy: str – proxy used for this run ("host:port" or full URL)
    recipe: str – name of the recipe (e.g. "Cointiply")
    result: str – "WIN", "FAIL", "CAPTCHA", "ERROR"
    sats: int – amount of satoshis earned (0 if none)
    details: str – optional free‑form text (error trace, captcha info, …)
    """
    _ensure_db()
    with _DB_LOCK:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO runs (ts, proxy, recipe, result, sats, details) VALUES (?,?,?,?,?,?)",
            (datetime.utcnow().isoformat(), proxy, recipe, result, sats, details)
        )
        conn.commit()
        conn.close()

def get_summary(days: int = 7):
    """Return a simple aggregation of the last *days* days.
    Returns a list of tuples: (date, total_sats, win_count, fail_count)."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DATE(ts) as d,
               SUM(sats) as total_sats,
               SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) as wins,
               SUM(CASE WHEN result!='WIN' THEN 1 ELSE 0 END) as fails
        FROM runs
        WHERE ts >= datetime('now', ?)
        GROUP BY d
        ORDER BY d DESC
        """,
        (f"-{days} days",)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
