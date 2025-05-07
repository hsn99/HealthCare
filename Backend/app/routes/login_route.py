from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.models.patient import Patient
from app.crud.auth_crud import get_fingerprint, finger, enroll_new_user
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/login/fingerprint")
def fingerprint_login(db: Session = Depends(get_db)):
    matched_id = get_fingerprint()

    if matched_id is None:
        raise HTTPException(status_code=401, detail="Fingerprint not recognized")

    user = db.query(Patient).filter(Patient.fingerprint_id == matched_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Welcome {user.name}",
            "user": {
                "id": user.id,
                "name": user.name,
            },
            "confidence": finger.confidence,
        },
    )


@router.post("/logout")
def logout_user():
    global is_logged_in, stop_scanning
    is_logged_in = False
    stop_scanning = False
    return {"message": "Logged out. Fingerprint scanner re-enabled."}


@router.post("/patients/enroll")
def enroll_fingerprint_for_patient(db: Session = Depends(get_db)):
    return enroll_new_user(db)
