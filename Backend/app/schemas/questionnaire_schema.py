from typing import List, Optional
from pydantic import BaseModel, field_validator
from .doctor_schema import DoctorOut
import json


class QuestionnaireBase(BaseModel):
    response: str


class QuestionnaireCreate(QuestionnaireBase):
    pass
    # patient_id: Optional[int] = None
    # assigned_doctor_id: Optional[int] = None
    # assigned_room_id: Optional[int] = None


class QuestionnaireOut(QuestionnaireBase):
    assigned_doctor: Optional[DoctorOut] = None
    assigned_room: Optional[int] = None

    model_config = {"from_attributes": True}

    # @field_validator("answers", mode="before")
    # def parse_answers(cls, v):
    #     if isinstance(v, str):
    #         return json.loads(v)
    #     return v
