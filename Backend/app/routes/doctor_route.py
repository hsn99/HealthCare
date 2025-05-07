# routes/patient_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.crud.doctor_crud import create_doctor, read_doctors, update_doctor
from app.schemas.doctor_schema import DoctorCreate, DoctorOut

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorOut)
def create(patient: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, patient)


@router.post("/{id}", response_model=DoctorOut)
def update(patient: DoctorCreate, id: int, db: Session = Depends(get_db)):
    return update_doctor(db, id, patient)


@router.get("/", response_model=list[DoctorOut])
def read(db: Session = Depends(get_db)):
    return read_doctors(db)


# @router.get("/{id}", response_model=PatientOut)
# def read_patient(id: int, db: Session = Depends(get_db)):
#     patient = get_patient_by_id(db, id)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     return patient
