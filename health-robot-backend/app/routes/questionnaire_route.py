# routes/patient_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from app.crud.questionnaire_crud import analyse_questions
from app.schemas.questionnaire_schema import QuestionnaireCreate, QuestionnaireOut

router = APIRouter(prefix="/questionnaire", tags=["Questionnaire"])


@router.post("/", response_model=QuestionnaireOut)
def create(questions: QuestionnaireCreate, db: Session = Depends(get_db)):
    return analyse_questions(db, questions)
