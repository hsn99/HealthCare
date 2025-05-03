# app/initialize_db.py

import sqlite3

def init_db():
    conn = sqlite3.connect("app_database.db")  # or whatever your database filename is
    cursor = conn.cursor()

    # Create the patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        weight REAL,
        temperature REAL,
        blood_pressure_systolic INTEGER,
        blood_pressure_diastolic INTEGER,
        pulse INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
