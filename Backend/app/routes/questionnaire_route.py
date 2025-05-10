# routes/patient_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from typing import Dict
from app.crud.questionnaire_crud import (
    analyse_questions,
    circulation_test,
    exposure_test,
)
from app.schemas.questionnaire_schema import QuestionnaireCreate, QuestionnaireOut

router = APIRouter(prefix="/questionnaire", tags=["Questionnaire"])


@router.post("/")
def create(data: Dict, db: Session = Depends(get_db)):
    return analyse_questions(db, data)


@router.get("/Circulation")
def handle_measurement():
    return circulation_test()


@router.get("/Exposure")
def handle_measurement():
    return exposure_test()
