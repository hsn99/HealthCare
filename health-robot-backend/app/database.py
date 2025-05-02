import sqlite3

# Initialize database connection
conn = sqlite3.connect("healthcare.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    temperature REAL,
    weight REAL,
    blood_pressure TEXT,
    pulse INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Store weight from MQTT
def store_weight(value):
    cursor.execute("INSERT INTO weights (value) VALUES (?)", (value,))
    conn.commit()

# Save patient profile
def save_patient(data):
    cursor.execute("""
        INSERT OR REPLACE INTO patients (patient_id, temperature, weight, blood_pressure, pulse)
        VALUES (?, ?, ?, ?, ?)
    """, (data.patient_id, data.temperature, data.weight, data.blood_pressure, data.pulse))
    conn.commit()

def get_all_patients():
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    # Debugging: Print rows to check the structure
    print(rows)
    
    return rows


# Function to get the latest weight
def get_latest_weight():
    cursor.execute("SELECT value FROM weights ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else None
