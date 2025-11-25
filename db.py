import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file="data.db"):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_measurement(self, temperature, humidity):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO measurements (timestamp, temperature, humidity) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), temperature, humidity)
        )
        conn.commit()
        conn.close()

    def query(self, sql, params=()):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
