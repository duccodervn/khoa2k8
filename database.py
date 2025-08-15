# database.py
import sqlite3

DB_NAME = "keys.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            ip TEXT PRIMARY KEY,
            key TEXT,
            expire_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
