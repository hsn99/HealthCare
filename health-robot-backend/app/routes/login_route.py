from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.models.patient import Patient
from app.crud.auth_crud import get_fingerprint, finger


router = APIRouter()


@router.post("/login/fingerprint")
def fingerprint_login(db: Session = Depends(get_db)):
    if get_fingerprint():
        user = (
            db.query(Patient).filter(Patient.fingerprint_id == finger.finger_id).first()
        )
        if user:
            return {
                "message": f"Welcome {user.name}",
                "user_id": user.id,
                "confidence": finger.confidence,
            }
        raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Fingerprint not recognized")


@router.post("/logout")
def logout_user():
    global is_logged_in, stop_scanning
    is_logged_in = False
    stop_scanning = False
    return {"message": "Logged out. Fingerprint scanner re-enabled."}
