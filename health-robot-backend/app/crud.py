from sqlalchemy.orm import Session
from app import models

def save_weight(db: Session, patient_id: int, weight: float):
    reading = models.PatientReading(
        patient_id=patient_id,
        weight=weight
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

def save_temperature(db: Session, patient_id: int, temperature: float):
    reading = models.PatientReading(
        patient_id=patient_id,
        temperature=temperature
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

def save_blood_pressure(db: Session, patient_id: int, systolic: int, diastolic: int, pulse: int):
    reading = models.PatientReading(
        patient_id=patient_id,
        systolic=systolic,
        diastolic=diastolic,
        pulse=pulse
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading
