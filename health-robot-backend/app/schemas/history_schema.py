from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DiseaseHistoryBase(BaseModel):
    disease_name: str
    description: Optional[str] = None
    date_diagnosed: Optional[datetime] = None


class DiseaseHistoryCreate(DiseaseHistoryBase):
    pass


class DiseaseHistoryOut(DiseaseHistoryBase):
    id: int

    model_config = {"from_attributes": True}
