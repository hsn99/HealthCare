from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room_schema import RoomCreate


def create_room(db: Session, room_data: RoomCreate):
    room = Room(**room_data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
