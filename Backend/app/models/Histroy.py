from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from ..db.database import Base


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)

    patients = relationship("patients", back_populates="medical_history")
