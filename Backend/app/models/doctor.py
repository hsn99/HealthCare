from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))

    patients = relationship("Patient", back_populates="doctor")

    room = relationship("Room", back_populates="doctors")
