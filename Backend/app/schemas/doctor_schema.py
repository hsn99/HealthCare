from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    room_id: int


class DoctorOut(DoctorBase):
    id: int
    room_id: int

    model_config = ConfigDict(from_attributes=True)
