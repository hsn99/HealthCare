from pydantic import BaseModel


class RoomBase(BaseModel):
    room_number: str
    waiting_time: str


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int

    model_config = {"from_attributes": True}
