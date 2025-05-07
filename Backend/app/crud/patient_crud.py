# crud/patient_crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate


def create_patient(db: Session, patient_data: PatientCreate):
    patient = Patient(**patient_data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def read_patients(db: Session):
    return db.query(Patient).all()


def update_patient(db: Session, patient_id: int, patient_data: PatientCreate):
    doctor = db.query(Patient).filter(Patient.id == patient_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.name = patient_data.name
    doctor.age = patient_data.age
    doctor.gender = patient_data.gender
    doctor.weight = patient_data.weight
    doctor.height = patient_data.height
    doctor.contact_info = patient_data.contact_info

    db.commit()
    db.refresh(doctor)
    return doctor
