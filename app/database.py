import sqlite3
import os

DB_NAME = "codes.db"

def init_db():
    # Create database if it doesn't exist
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create a simple table for CPT/HCPCS codes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS codes (
        code TEXT PRIMARY KEY,
        description TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized and ready!")

def add_code(code, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO codes (code, description) VALUES (?, ?)", (code, description))
    conn.commit()
    conn.close()

def get_code(code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code, description FROM codes WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result
