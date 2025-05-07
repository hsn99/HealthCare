from typing import Optional
from pydantic import BaseModel, ConfigDict
from .room_schema import RoomOut


class DoctorBase(BaseModel):
    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int
    room_id: Optional[int]
    room: Optional[RoomOut] = None

    model_config = ConfigDict(from_attributes=True)
