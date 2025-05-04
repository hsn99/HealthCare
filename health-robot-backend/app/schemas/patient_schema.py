from pydantic import BaseModel
from typing import List, Optional

from app.schemas.doctor_schema import DoctorOut
from app.schemas.room_schema import RoomOut
from app.schemas.history_schema import DiseaseHistoryOut


class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    contact_info: Optional[str] = None
    weight: float
    height: float


class PatientCreate(PatientBase):
    doctor_id: Optional[int] = None
    room_id: Optional[int] = None
    fingerprint_id: Optional[int] = None


class PatientOut(PatientBase):
    id: int
    doctor: Optional[DoctorOut]
    room: Optional[RoomOut]
    disease_history: List[DiseaseHistoryOut] = []
    fingerprint_id: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
