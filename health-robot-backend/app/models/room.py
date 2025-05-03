from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..db.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True)
    waiting_time = Column(String)

    patients = relationship("Patient", back_populates="room")

    doctors = relationship("Doctor", back_populates="room")
