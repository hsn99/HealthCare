# routes/patient_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.crud.patient_crud import (
    create_patient,
    get_patient_by_id,
    read_patients,
    get_patient_weight,
)
from app.schemas.patient_schema import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientOut)
def create(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, patient)


@router.post("/weight")
def get_weight():
    return get_patient_weight()


@router.get("/", response_model=list[PatientOut])
def read(db: Session = Depends(get_db)):
    return read_patients(db)


@router.get("/{id}", response_model=PatientOut)
def read_patient(id: int, db: Session = Depends(get_db)):
    patient = get_patient_by_id(db, id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
