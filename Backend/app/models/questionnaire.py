from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..db.database import Base
from app.models.room import Room


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    answers = Column(Text)
    assigned_doctor_id = Column(Integer, ForeignKey("doctors.id"))
    assigned_room_id = Column(Integer, ForeignKey("rooms.id"))

    patient = relationship("Patient", back_populates="questionnaire")
    assigned_doctor = relationship("Doctor")
    assigned_room = relationship(Room)
