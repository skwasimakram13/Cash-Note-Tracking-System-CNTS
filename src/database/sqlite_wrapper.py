import sqlite3
from src.core.config import Config
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self._create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Operators
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                login_id TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Insert default operator if empty
        cursor.execute("SELECT count(*) FROM operators")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO operators (name, login_id) VALUES (?, ?)", ("Default Admin", "admin"))
            conn.commit()

        # Notes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                serial_number TEXT PRIMARY KEY,
                denomination INTEGER NOT NULL,
                status TEXT NOT NULL, -- IN, OUT
                last_seen TIMESTAMP,
                created_at TIMESTAMP
            )
        ''')

        # Transactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL, -- IN, OUT
                total_amount INTEGER NOT NULL,
                operator_id INTEGER,
                timestamp TIMESTAMP,
                FOREIGN KEY(operator_id) REFERENCES operators(id)
            )
        ''')
        
        conn.commit()
        conn.close()

# Global instance
db = Database()
