from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
from app.models.patient import Patient


class DiseaseHistory(Base):
    __tablename__ = "disease_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    disease_name = Column(String)
    description = Column(Text)
    date_diagnosed = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="disease_history")
