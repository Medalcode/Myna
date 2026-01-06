"""
Hermes Database Module - Unified SQLite Management
Handles all data persistence for the bot: runs, earnings, and statistics.
"""

import os
import sqlite3
import threading
from datetime import datetime, timedelta

# Database path - now in dedicated data/ directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hermes.db')
_DB_LOCK = threading.Lock()


class HermesDB:
    """Unified database manager for Hermes bot"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self._ensure_db()
    
    def _ensure_db(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with _DB_LOCK:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            # Table 1: Execution runs (detailed log of each recipe execution)
            cur.execute('''
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    proxy TEXT,
                    recipe TEXT,
                    result TEXT,
                    sats INTEGER DEFAULT 0,
                    details TEXT
                )
            ''')
            
            # Table 2: Earnings summary (aggregated earnings per session/recipe)
            cur.execute('''
                CREATE TABLE IF NOT EXISTS earnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    recipe TEXT,
                    amount INTEGER,
                    proxy TEXT,
                    status TEXT
                )
            ''')
            
            # Table 3: Proxy health tracking
            cur.execute('''
                CREATE TABLE IF NOT EXISTS proxy_health (
                    proxy TEXT PRIMARY KEY,
                    last_success TEXT,
                    last_failure TEXT,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def log_run(self, session_id: str, proxy: str, recipe: str, result: str, 
                sats: int = 0, details: str = ""):
        """
        Log a single recipe execution.
        
        Args:
            session_id: Unique session identifier (e.g., "account_001")
            proxy: Proxy used (e.g., "http://1.2.3.4:8080")
            recipe: Recipe name (e.g., "Cointiply")
            result: Execution result ("WIN", "FAIL", "CAPTCHA", "ERROR")
            sats: Satoshis earned (0 if failed)
            details: Additional information or error message
        """
        with _DB_LOCK:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO runs 
                   (timestamp, session_id, proxy, recipe, result, sats, details) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (datetime.utcnow().isoformat(), session_id, proxy, recipe, 
                 result, sats, details)
            )
            conn.commit()
            conn.close()
    
    def log_earning(self, session_id: str, recipe: str, amount: int, 
                    proxy: str, status: str = "SUCCESS"):
        """
        Log an earning event (legacy compatibility with old oracle system).
        
        Args:
            session_id: Session identifier
            recipe: Recipe name
            amount: Amount earned in satoshis
            proxy: Proxy used
            status: Status message
        """
        with _DB_LOCK:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO earnings 
                   (timestamp, session_id, recipe, amount, proxy, status) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (datetime.utcnow().isoformat(), session_id, recipe, amount, 
                 proxy, status)
            )
            conn.commit()
            conn.close()
    
    def update_proxy_health(self, proxy: str, success: bool):
        """Update proxy health status after each use"""
        with _DB_LOCK:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            now = datetime.utcnow().isoformat()
            
            # Check if proxy exists
            cur.execute("SELECT * FROM proxy_health WHERE proxy = ?", (proxy,))
            exists = cur.fetchone()
            
            if exists:
                if success:
                    cur.execute(
                        """UPDATE proxy_health 
                           SET last_success = ?, success_count = success_count + 1 
                           WHERE proxy = ?""",
                        (now, proxy)
                    )
                else:
                    cur.execute(
                        """UPDATE proxy_health 
                           SET last_failure = ?, failure_count = failure_count + 1 
                           WHERE proxy = ?""",
                        (now, proxy)
                    )
            else:
                # Insert new proxy
                if success:
                    cur.execute(
                        """INSERT INTO proxy_health 
                           (proxy, last_success, success_count) 
                           VALUES (?, ?, 1)""",
                        (proxy, now)
                    )
                else:
                    cur.execute(
                        """INSERT INTO proxy_health 
                           (proxy, last_failure, failure_count) 
                           VALUES (?, ?, 1)""",
                        (proxy, now)
                    )
            
            conn.commit()
            conn.close()
    
    def get_stats(self, days: int = 7):
        """
        Get statistics for the last N days.
        
        Returns:
            dict: Statistics including total sats, today's earnings, win/fail counts
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Total all-time earnings
        cur.execute("SELECT COALESCE(SUM(sats), 0) FROM runs WHERE result = 'WIN'")
        total_sats = cur.fetchone()[0]
        
        # Today's earnings
        today = datetime.utcnow().date().isoformat()
        cur.execute(
            """SELECT COALESCE(SUM(sats), 0) FROM runs 
               WHERE result = 'WIN' AND DATE(timestamp) = ?""",
            (today,)
        )
        today_sats = cur.fetchone()[0]
        
        # Win/Fail counts (last N days)
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        cur.execute(
            """SELECT 
                   SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins,
                   SUM(CASE WHEN result != 'WIN' THEN 1 ELSE 0 END) as fails
               FROM runs 
               WHERE timestamp >= ?""",
            (since,)
        )
        wins, fails = cur.fetchone()
        
        conn.close()
        
        return {
            'total': total_sats,
            'today': today_sats,
            'wins': wins or 0,
            'fails': fails or 0,
            'success_rate': round((wins / (wins + fails) * 100) if (wins + fails) > 0 else 0, 2)
        }
    
    def get_summary(self, days: int = 7):
        """
        Get daily summary for the last N days.
        
        Returns:
            list: List of tuples (date, total_sats, wins, fails)
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        cur.execute(
            """SELECT 
                   DATE(timestamp) as date,
                   SUM(sats) as total_sats,
                   SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins,
                   SUM(CASE WHEN result != 'WIN' THEN 1 ELSE 0 END) as fails
               FROM runs
               WHERE timestamp >= ?
               GROUP BY DATE(timestamp)
               ORDER BY date DESC""",
            (since,)
        )
        
        rows = cur.fetchall()
        conn.close()
        
        return rows


# Global instance for backward compatibility
oracle = HermesDB()
