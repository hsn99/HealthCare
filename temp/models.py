from pydantic import BaseModel
import sqlite3

class PatientReadings(BaseModel):
    patient_id: str
    temperature: float
    weight: float
    blood_pressure: str
    pulse: int
import sqlite3

def save_patient_reading(reading):
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patient_readings (patient_id, temperature, weight, blood_pressure, pulse)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            reading.patient_id,
            reading.temperature,
            reading.weight,
            reading.blood_pressure,
            reading.pulse
        )
    )
    conn.commit()
    conn.close()
