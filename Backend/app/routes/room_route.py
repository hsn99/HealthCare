from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.crud.room_crud import create_room
from app.schemas.room_schema import RoomCreate, RoomOut

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomOut)
def create(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room(db, room)


# @router.get("/", response_model=list[PatientOut])
# def read(db: Session = Depends(get_db)):
#     return read_patients(db)


# @router.get("/{id}", response_model=PatientOut)
# def read_patient(id: int, db: Session = Depends(get_db)):
#     patient = get_patient_by_id(db, id)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     return patient
