from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base
from app.models.questionnaire import Questionnaire


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    fingerprint_id = Column(Integer, unique=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    weight = Column(Float)
    height = Column(Integer)

    contact_info = Column(String)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

    doctor = relationship("Doctor", back_populates="patients")
    room = relationship("Room", back_populates="patients")
    disease_history = relationship(
        "DiseaseHistory", back_populates="patient", cascade="all, delete-orphan"
    )
    questionnaire = relationship(
        "Questionnaire", back_populates="patient", uselist=False
    )
