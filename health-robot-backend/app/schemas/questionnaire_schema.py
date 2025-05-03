from typing import List, Optional
from pydantic import BaseModel, field_validator
from .doctor_schema import DoctorOut
from .room_schema import RoomOut
import json


class QuestionnaireBase(BaseModel):
    answers: List[str]


class QuestionnaireCreate(QuestionnaireBase):
    patient_id: Optional[int] = None
    assigned_doctor_id: Optional[int] = None
    assigned_room_id: Optional[int] = None


class QuestionnaireOut(QuestionnaireBase):
    id: int
    assigned_doctor: Optional[DoctorOut] = None
    assigned_room: Optional[RoomOut] = None

    model_config = {"from_attributes": True}

    @field_validator("answers", mode="before")
    def parse_answers(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
