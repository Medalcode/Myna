import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'olympus.db')

class Oracle:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Inicializa las tablas si no existen."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                recipe TEXT,
                amount INTEGER,
                proxy TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def log_earning(self, session_id, recipe, amount, proxy, status="SUCCESS"):
        """Registra una ganancia o intento."""
        self.cursor.execute('''
            INSERT INTO earnings (session_id, recipe, amount, proxy, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, recipe, amount, proxy, status))
        self.conn.commit()

    def get_total_earnings(self):
        """Devuelve el total histórico de satoshis."""
        self.cursor.execute('SELECT SUM(amount) FROM earnings WHERE status="SUCCESS"')
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def get_today_earnings(self):
        """Devuelve las ganancias desde las 00:00 de hoy."""
        self.cursor.execute('''
            SELECT SUM(amount) FROM earnings 
            WHERE status="SUCCESS" 
            AND date(timestamp) = date('now')
        ''')
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def get_stats(self):
        return {
            "total": self.get_total_earnings(),
            "today": self.get_today_earnings()
        }

# Instancia global para ser usada por los bots
oracle = Oracle()
