from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.models.patient import Patient
from app.crud.auth_crud import (
    get_fingerprint,
    finger,
    enroll_new_user,
    patient_logout,
    patient_login,
)

router = APIRouter()


@router.post("/login/fingerprint")
def fingerprint_login(db: Session = Depends(get_db)):
    return patient_login(db)


@router.post("/logout")
def logout_user():
    return patient_logout()


@router.post("/patients/enroll")
def enroll_fingerprint_for_patient():
    return enroll_new_user()
