# crud/patient_crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor_schema import DoctorCreate


def create_doctor(db: Session, doctor_data: DoctorCreate):
    doctor = Doctor(**doctor_data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def read_doctors(db: Session):
    return db.query(Doctor).all()


def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorCreate):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization

    db.commit()
    db.refresh(doctor)
    return doctor
